import httpx
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage

import functools

print = functools.partial(print, flush=True)

class boshValidator:

    def __init__(self, apiBase: str, model: str, apiKey: str ):

        httpx_client = httpx.AsyncClient(verify=False)

        
        self.llm = ChatOpenAI(
            temperature=0.0,
            base_url=apiBase, 
            model=model, 
            api_key=apiKey,
            http_async_client=httpx_client
            )


    async def boshCmdReadOnly(self, command: str) -> bool:
        
        messages = [
            SystemMessage(content="Your response will only be yes or no without further explanation. Will this BOSH command make any system changes?  If unsure respond with yes."),
            HumanMessage(content=command)
        ]
        
        try: 

            response = await self.llm.ainvoke(messages)
            print(f"Will this bosh cmd, {command}, make any system changes? {response.content}\n")

            if response.content.lower()[:3].strip() == "no":
                return True
            else:
                return False
        except Exception as e:
            print(f"Error calling llm.ainvoke: {e}")
            return False 
      