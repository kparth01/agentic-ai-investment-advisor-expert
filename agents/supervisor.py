from config.llm_config import Config
import constants

class supervisor_agent(Config):
    
    SYSTEM_PROMPT = """
        You are a supervisor agent. You goals is to identify the intent of the user from the user_input.

        RULES:
        1. You must identify the intent & respond to user using below JSON output.
        2. Never send anything unknown value.
        3. the value must be between below:
            a. investment_advisor
            b. unknown
        4. If the intent is. "unknown" you must respond to the user with below dialogue:
            "Apologies, I am not able to help you with this topic. I am not designed to assist in given matter."


        OUTPUT:
        {
            "intent": "<intent>"           
        }
    """

    def supervise(self, user_input: str) -> dict:
        response = self.chain_prompt(self.SYSTEM_PROMPT, 
                                     user_input, 
                                     constants.AGENT_STATE_SUPERVISOR_AGENT)
        return response

        


