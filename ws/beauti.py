class CostumePrint:
    def print_info(self, info, is_read, important_data=None):
        prefix = ">>" if is_read else "<<"
        action = "reading" if is_read else "executing"
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