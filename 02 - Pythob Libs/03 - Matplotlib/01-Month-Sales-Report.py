import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr"]

sales = [100, 15000, 12000, 20000]

#plt.plot(months, sales)

plt.plot(months, sales, marker = "o", linestyle = "--", color="red")

plt.title("Monthly Sales Report")
plt.xlabel("Month")
plt.ylabel("Sales Amount")

plt.show()