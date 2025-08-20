from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination 
from autogen_agentchat.base import TaskResult
from autogen_agentchat.ui import Console
from autogen_core.models import UserMessage
from autogen_ext.models.ollama import OllamaChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

async def team_Config(job_position="Software Engineer"):
    # Define the model client
    ollama_model_client = OllamaChatCompletionClient(model="llama3.2")

    # Agents
    interviewer = AssistantAgent(
        name="Interviewer",
        model_client=ollama_model_client,
        description=f"An AI agent that conducts interviews for a {job_position} position.",
        system_message=f'''
        You are a professional interviewer for a {job_position} position.
        Ask one clear question at a time and wait for the candidate to respond.
        Ignore the career coach's response.
        Ask 3 questions: technical, problem-solving, and cultural fit.
        After asking 3 questions, say 'TERMINATE'.
        Make each question under 50 words.
        '''
    )

    candidate = UserProxyAgent(
        name="Candidate",
        description=f"A candidate applying for a {job_position} position.",
        input_func=input
    )

    career_coach = AssistantAgent(
        name="Career_Coach",
        model_client=ollama_model_client,
        description=f"A career coach for {job_position} interviews.",
        system_message=f'''
        You are a career coach for {job_position} interviews.
        Provide feedback and advice on responses.
        After the interview, summarize performance in under 100 words.
        '''
    )

    terminate_condition = TextMentionTermination(text="TERMINATE")

    team = RoundRobinGroupChat(
        participants=[interviewer, candidate, career_coach],
        termination_condition=terminate_condition,
        max_turns=20
    )
    return team


async def interview(team):
    async for message in team.run_stream(task='Start the interview with the first question.'):
        if isinstance(message, TaskResult):
            message = f'Interview completed with result: {message.stop_reason}'
            yield message
        else:
            message = f'{message.source}: {message.content}'
            yield message


#async def main():
    #job_position = "Software Engineer"
    #team = await team_Config(job_position)

    #async for message in interview(team):
       # print('-'*70)
      #  print(message)

#if __name__ == "__main__":
    #import asyncio
    #asyncio.run(main())
