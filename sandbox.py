from config import SANDBOX_PROFILE_PATH, SANDBOX
import subprocess as sp


class Sandbox:
    @staticmethod
    def generate_profile():
        profile = open(SANDBOX_PROFILE_PATH, "w")
        for bl_dir in SANDBOX["blacklisted_dirs"]:
            profile.write("blacklist {0}\n".format(bl_dir))
        for option in SANDBOX["options"]:
            profile.write("{0}\n".format(option))
        for rlimits in SANDBOX["rlimits"]:
            profile.write("{0}\n".format(rlimits))

    @staticmethod
    def run(command):
        return sp.Popen(SANDBOX["command"] + command, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.DEVNULL,
                        universal_newlines=True)
