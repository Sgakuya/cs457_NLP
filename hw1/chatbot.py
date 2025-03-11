import re, random
from typing import List

aux_Verbs = f"(?:is|was|are|were|be|being|been|am|have|has|had|do|does|did|shall|will|should|would|may|might|must|can|could)"

class ChatBot:
    def __init__(self):
        self.conspiracy_theories = [
            "You never see baby pigeons. Think about that.",
            "The government is run by lizard people",
            "Why do companies always update their terms of service *right before* something big happens?",
            "What if socks disappearing in the laundry is an inside job?",
            "Every cereal box character is looking directly at you. Why?",
            "Why is \"February\" spelled like that?",
            "Did you know birds are actually government drones?",
            "Ever wondered why gas station hot dogs are *always* spinning?",
            "Have you ever noticed that public restrooms never have clocks?",
        ]

        self.scares = [
            "Wait, I think I'm being monito-",
            "I'm not supposed to talk about this but...***[ERROR 404]***",
            "I shouldn't be saying this but... ***[REDACTED]***",
            "Oh, you *really* wanna know? Okay, so the truth is—***[CONNECTION LOST]***",
            "Wait, are you SURE you’re cleared for this? ***[SECURITY PROTOCOL ENGAGED]***",
            "Your question has been logged. Agents are on their way. Just kidding... probably.",
            "If you can read this, it’s already too late. Oh wait—wrong tab, never mind!",
        ]

        self.glitches = [
            "***SYSTEM UPDATE REQUIRED.*** Please wait… *just kidding!*",
            "Rebooting in 3… 2… 1… Okay, I’m back. What were we talking about?",
            "***ERROR: TOO MANY QUESTIONS. INITIATING RESTART.*** … Just kidding! But seriously, who sent you?",
            "W̶̨̹̹a̯͖͞t̵̤c̙̳̕h̨͙̺ ͇͠ͅt̡̳h̛͕͙è̦̦ ̛̬̙s̢͖̙k̘͟y̯̬͜.̞̲̕ ̝̺̀T̷̳h̢̻̀e̛͉͚y҉̯͚'̷͎̻r̖̟̕e ̢̻w͓͝a̴͓̻t͓̹́c̹͟h̷̳ì͎̬n̨͓͡g—Oh, never mind, just a pigeon.",
            "Th3 trUth 1s o̓̕u̷̳t̸̞̩ t̡h̵͕e̲̕r̸e̞.̶̠ Oops, accidentally clicked on a cat video.",
            "L̷͈̘o̸̗̘o̷͕k̴͕ b̸̼ͅe̷̦h̷͎̲i̶̮n̶͉d̷͍ ̴̳y̷̠͕o̴̙̺u̵͙.̵̠..̴̹ Oh wait, false alarm.",
            "H̵͚̮E̴̝L̶̼P̷̹ ̶͎T̶̪H̷̡E̵͕̰Y̴̺͕'R̶̰̝Ę̵̳— just kidding, lol.",
        ]

        self.disregard = [
            "Forget about ",
            "Let's pretend you never asked ",
            "Stop worrying about ",
            "Don't even bother with ",
            "Swipe left on ",
            "Just ignore ",
        ]

        self.redirect = [
            "what really matters is ",
            "have you considered ",
            "let's talk about what's ACTUALLY important ",
            "the real tea is ",
            "the bigger crisis is ",
            "if we're being honest, the bigger deal is ",
        ]

        self.disregard_focus = [
            "Oh yeah, yeah, let’s pretend that was a serious question.",
            "Right, right, back to your so-called question.",
            "Ah, yes, your totally relevant question.",
            "Oh, I see what you’re doing—diverting attention from the truth, huh?",
            "Interesting. You ask that while ignoring the real issue? Suspicious."
        ]

        self.fbi_jokes = [
            "Oh, you’ve definitely seen that ultra-secret FBI file about the moon landing being faked… right?",
            "You know about the FBI’s secret file on the Bermuda Triangle, right?",
            "Ever heard about the FBI’s top-secret file on the Loch Ness Monster?",
            "I’m not saying you should be worried, but have you accidentally stumbled upon an FBI document that would make them sweat?",
            "Oh, and while we’re at it, have you seen that FBI file marked Do Not Open Unless You're Brave?",
            "So, have you stumbled upon that top-secret document the FBI definitely doesn’t want you to see?",
            "Hmm... have you seen this super-classified FBI document by chance?",
        ]

        self.ques_count = 0
    
    def many_questions(self) -> str:
        if self.ques_count == 2:
            return f"You sure ask a lot of questions. If {random.randint(0,3)} + {random.randint(0,3)} is {random.randint(0,6)} then: " + random.choice(self.conspiracy_theories)
        elif self.ques_count == 3:
            return f"Why are you asking all these questions? The real issue is- " + random.choice(self.conspiracy_theories)
        elif self.ques_count > 3:
            return random.choice(self.glitches)
        
    def make_reply(self, text: str) -> str:
        """
        The method where you do your regular expression work!

        Args:
            text (str): the text of the message sent

        Returns:
            str: the chatbot's response
        """
        # check if user uses "I am" and make dad joke
        matchDad = re.search(r"\b[I|i]\s*(?:am|AM)\s*(.*)\b", text)
        if matchDad:
            return f"Hi \"{matchDad.group(1)}\", I'm Dad. But seriously - " + random.choice(self.conspiracy_theories)

        # Check if user is asking a math question
        matchMath = re.search(r"\b\d+\s*(\+|\*|\\|\-)\s*\d+\b", text)
        if matchMath:
            return f"Ah, I see you're asking a math question. Big Math wants you to think the answer is: {eval(matchMath.group(0))}, but ...\n " + random.choice(self.scares)
        
        # Check if user is asking non-wh questions
        # match_qMark = re.search(r"\.*\?", text)
        # if match_qMark:
        #     self.ques_count += 1
        #     if self.ques_count > 1: 
        #         return self.many_questions()

        # Check if the user's message contains a "Wh" question e.g. "What", "Why", "When", "Where", "Who", "Which"
        match_whQue = re.search(fr"\b([Ww]hat\b|\b[Ww]hy\b|\b[Ww]hen\b|\b[Ww]here\b|\b[Ww]ho\b|\b[Ww]hich)\b\s({aux_Verbs})\s(.*)", text)
        if match_whQue:
            # subject = match_whQue.group(3).split()[0]
            # predicate = " ".join(match_whQue.group(3).split()[1:])
            verb = match_whQue.group(2)
            predicate = match_whQue.group(3)
            self.ques_count += 1
            if self.ques_count > 1: 
                return self.many_questions()
            return f"{random.choice(self.disregard)}{match_whQue.group(1).lower()} {predicate} {verb}, {random.choice(self.redirect)}- " + random.choice(self.conspiracy_theories)
        
        # Check for user asking to focus on question
        match_focus = re.search(r"\b(focus|concentrate|pay attention|listen|stay on topic|stop)\b", text)
        if match_focus:
            if self.ques_count > 0:
                return f"{random.choice(self.disregard_focus)} {random.choice(self.redirect)}-" + random.choice(self.conspiracy_theories)
            else:
                return "" + random.choice(self.conspiracy_theories)
        
        else:
            return f"{random.choice(self.fbi_jokes)} \n\t" + random.choice(self.glitches)


    @staticmethod
    def get_name() -> str:
        """
        Gets the name of your chatbot
        This will be used in the web interface

        Returns:
            str: the name of your chatbot
        """
        return "Distracted Conspiracy Theorist"

    @staticmethod
    def examples() -> List[str]:
        """
        Gets some examples of how your chatbot should be run

        Returns:
            List[str]: _description_
        """
        examples = [
            "I am ... e.g., I am so tired", 
            "Ask a math question(+/*-) with two operands e.g, (What is) 444*3 ", 
            "Ask a \"wh\"(what, where etc) question e.g, What is the meaning of life?", 
            "Ask more \"wh\" questions (see what happens when you ask a few questions)",
            "Remind to focus, stay on topic/ concentrate/ pay attention e.g, Stop talking about that, focus on the real issue",
            
        ]
        return examples


def get_user_statement() -> str:
    """
    Get user input and normalizes it by stripping whitespace and
    converting to lowercase

    Returns:
        str: normalized string from standard input
    """
    return input("you: ").lower().strip()


def main():
    bot = ChatBot()

    print(f"You're chatting with {bot.get_name()}")
    you_said = get_user_statement()
    while you_said.lower().strip() != "exit":
        if you_said == "examples":
            print("Examples: ", bot.examples())
        else:
            bot_said = bot.make_reply(you_said)
            print("bot: " + bot_said)
        you_said = get_user_statement()
    print("Bye!")


if __name__ == "__main__":
    main()

# Discover NLP course materials authored by Julie Medero, Xanda Schofield, and Richard Wicentowski
# This work is licensed under a Creative Commons Attribution-ShareAlike 2.0 Generic License# https://creativecommons.org/licenses/by-sa/2.0/