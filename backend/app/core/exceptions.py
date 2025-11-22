class AgentError(Exception):
    pass

class CodeParseError(AgentError):
    pass

class GitHubSearchError(AgentError):
    pass

class LLMError(AgentError):
    pass
