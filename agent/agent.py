from langchain_core.messages import ToolMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated, Generator
import logging
from .tools.spotify_tools import *
from .models import qwen35_flash, gpt_oss_120b, llama4_Scout
from .prompt import system_prompt

from .tools.spotify_controller import sc

logger = logging.getLogger(__name__)

tools = [pause, 
         resume, 
         next_track, 
         previous_track,
         get_playlists, 
         play_playlist_by_name,
         search_tracks,
         search_playlists,
         search_albums,
         play_track_by_id,
         play_playlist_by_id,
         play_album_by_id,
         set_repeat,
         set_shuffle]

available_tools = {t.name: t for t in tools}

graph_break_tools = ["pause", 
                     "resume", 
                     "next_track", 
                     "previous_track", 
                     "play_playlist", 
                     "play_by_id",
                     "set_repeat",
                     "set_shuffle"]

model = qwen35_flash.bind_tools(
    tools = tools
)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def agent_node(state):
    logger.debug("Executing agent_node")
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def tool_node(state):
    logger.debug("Executing tool_node")
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    tool_messages = []
    
    for tool_call in tool_calls:
        tool_name = tool_call['name']
        tool_to_call = available_tools.get(tool_name)
        
        if tool_to_call:
            logger.info(f"Tool execution: {tool_name}")
            response = tool_to_call.invoke(tool_call['args'])
            tool_messages.append(ToolMessage(content=str(response), name=tool_name, tool_call_id=tool_call['id']))
        else:
            logger.error(f"Tool not found: {tool_name}")
            tool_messages.append(ToolMessage(content=f"Error: tool '{tool_name}' not found.", name=tool_name, tool_call_id=tool_call['id']))
    
    return {"messages": tool_messages}

def router_after_tools(state):
    last_message = state["messages"][-1]
    
    if getattr(last_message, "name", "") in graph_break_tools:
        logger.info("[Router]: The graph was completed to save tokens")
        return END
    
    return "agent"

def should_continue(state):
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        logger.debug("Routing to action node")
        return "continue"
    logger.debug("Routing to end")
    return "end"

workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("action", tool_node)
workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

workflow.add_conditional_edges(
    "action",
    router_after_tools
)

graph = workflow.compile()


def request_to_agent(request: str)->str:
    current_state = sc.get_current_playback_info()
    logger.info(f"New request to agent: {request}")
    input_data = {"messages": [system_prompt.format(
        curr_state=f"""Device: {current_state["device"]}
        Is playing: {current_state["is_playing"]}
        Current track: {current_state["track"]}
        Playlist: {current_state["playlist"]}
        """), request]}
    res = graph.invoke(input=input_data)
    final_response = res["messages"][-1].content
    logger.info(f"Agent response: {final_response}")
    return final_response