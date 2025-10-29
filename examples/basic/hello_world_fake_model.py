import asyncio

from agents import Agent, Runner, set_tracing_disabled
from tests.fake_model import FakeModel
from openai.types.responses import ResponseOutputMessage, ResponseOutputText

# 禁用跟踪以简化输出
set_tracing_disabled(True)

# 创建使用 FakeModel 的 Agent
fake_model = FakeModel(
    initial_output=[
        ResponseOutputMessage(
            id="1",
            type="message",
            role="assistant",
            content=[
                ResponseOutputText(
                    text="Code within the code,\nFunctions calling themselves,\nInfinite loop's dance.",
                    type="output_text",
                    annotations=[]
                )
            ],
            status="completed"
        )
    ]
)

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=fake_model,
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
