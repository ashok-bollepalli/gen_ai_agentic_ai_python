class ChatBot:

    def welcome_user(self):
        print("Welcome to GEN AI Chatbot..")

    def collect_question(self, question):
        print("User Question : ", question)


class CustomerSupportBot(ChatBot):
    def solve_customer_issue(self):
        print("Solving Customer issue using AI")

class CourseCounsellingBot(ChatBot):
    def sugget_course(self):
        print("Suggesting Best Course Using Ai")


bot1 = CustomerSupportBot()
bot1.welcome_user()
bot1.collect_question("Why my outlook is not working ?")
bot1.solve_customer_issue()

print("--------------------------")

bot2 = CourseCounsellingBot()
bot2.welcome_user()
bot2.collect_question("Which course is best for me ?")
bot2.sugget_course()
