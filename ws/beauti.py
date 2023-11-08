class CostumePrint:

    def __init__(self):
        pass

    def explain_status_code(self, status_code)->str:
        """Explains status code

        Args:
            status_code (int): status code of request
        
        Return:
            description of the status code if is defined
        """
        explanations = {
            200: "OK {200}",
            201: "Created {201}",
            204: "No Content {204}",
            301: "Moved Permanently {301}",
            400: "Bad Request {400}",
            401: "Unauthorized {401}",
            403: "Forbidden {403}",
            404: "Not Found {404}",
            500: "Internal Server Error {500}",
            503: "Service Unavailable {503}"
        }
        explanation = explanations.get(status_code, "Unknown Status Code: Explanation not found.")
        return explanation


    def info(self, info, what, important_data=None):
        """prints what is going on in the program

        Args:
            info (str): what we wish to print
            what (int): where are we doing (
                0: informing about something that will be happening, 
                1: outputting the data,
                2: general info
                )
            important_data (str, optional): Any important information . Defaults to None.
        """
        avb_prefix = ['<<', '>>', '<>']
        avb_action = ['EXECUTING', 'READING', 'INFO']
        prefix = avb_prefix[what]
        action = avb_action[what]
        important_part = f"{important_data}" if important_data else None
        print(f"{prefix} [{action}] \t:: {info}") if important_part is None else print(
            f"{prefix} [{action}] \t:: !! {important_part} !!\n{prefix} [{action}] \t:: {info}")
        return
    def get_info(self, info):
        """prompts user for input

        Args:
            info (str): what we wish to print
        """
        prefix = "..."
        print(f"{prefix} [prompting] \t:: {info}\n")