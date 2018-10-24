import sys
from selenium import webdriver
import time
import discord
import asyncio

def mailpass():
    with open("mailpass.txt") as f:
        return f.read().strip().split(':')


async def sendBTC(amount, email, login=False):

    driver = webdriver.Chrome()

    if login:
        driver.get("https://hiribi.com/login")
        username, password = mailpass()
        login = driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[3]')
        if login.text.strip().lower == "login":
            mail = driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[1]/div/input')
            mail.send_keys(username)
            pwd = driver.find_element_by_xpath('/html/body/div/div/form/div[1]/div[2]/div/input')
            pwd.send_keys(password)
            login.click()
            time.sleep(2)

    driver.get("https://hiribi.com/")

    input = driver.find_element_by_xpath(
        '//*[@id="createRequestForm"]/div/div/div/div/div/div/div/form/div[1]/div[1]/div[2]/input')
    input.send_keys(amount)

    mail = driver.find_element_by_xpath(
        '//*[@id="createRequestForm"]/div/div/div/div/div/div/div/form/div[1]/div[3]/div[2]/input')
    mail.send_keys(email)

    submit = driver.find_element_by_xpath('//*[@id="uid50"]')
    submit.click()

    time.sleep(3)

    res_details = driver.find_element_by_xpath('//*[@id="sell"]/div/div/div/div/div[4]/div/div/div/div/div[2]/div/div/div/div/div/div[2]/div/div/div')
    res = res_details.text
    res += "\n\n**"
    res_crypto_transaction = driver.find_element_by_xpath('//*[@id="sell"]/div/div/div/div/div[4]/div/div/div/div/div[2]/div/div/div/div/div/div[4]')
    res += res_crypto_transaction.text
    res += "**"
    driver.close()

    return res


async def checkTransaction(transaction):
    driver = webdriver.Chrome()
    driver.get("https://hiribi.com/")

    input = driver.find_element_by_xpath('//*[@id="checkRequestForm"]/div/div/div/div/div/div/div/form/div[1]/div/div[2]/input')
    input.send_keys(transaction)

    button = driver.find_element_by_xpath('//*[@id="uid63"]/input')
    button.click()
    time.sleep(2)

    result = driver.find_element_by_xpath('//*[@id="checkRequestForm"]/div/div/div/div/h1')
    res = result.text

    driver.close()
    return res


async def getProfit():
    driver = webdriver.Chrome()
    driver.get("https://hiribi.com/")

    result = driver.find_element_by_xpath('//*[@id="createRequestForm"]/div/div/div/div/div/div/div/div[1]/div[1]/div/div/div/h1[2]/span[3]/span/span/strong')
    res = result.text

    driver.close()
    return res


def getToken():
    with open("discord_token.txt") as f:
        return f.read().strip()


def main(argc, argv):
    #sendBTC("0.2", "just@testing.com")
    #checkTransaction("8733caaad87dc5939638ac969855317c")
    client = discord.Client()

    @client.event
    async def on_ready():
        print('HiribiBot Logged in as')
        print("username: " + client.user.name)
        print("user_id: " + client.user.id)
        print('------')

    @client.event
    async def on_message(message):
        if message.content.startswith('!check ') and message.author.name != client.user.name:
            try:
                print(message.content)
                res = await checkTransaction(message.content.strip().split(" ")[1])
            except Exception as e:
                res = "error: {}".format(e)
            await client.send_message(message.channel, res)
        elif message.content.startswith("!send ") and message.author.name != client.user.name:
            try:
                print(message.content)
                res = await sendBTC(message.content.strip().split(" ")[1], message.content.strip().split(" ")[2], login=True)
            except Exception as e:
                res = "error: {}".format(e)
            await  client.send_message(message.channel, res)
        elif message.content.startswith("!profit") and message.author.name != client.user.name:
            try:
                print(message.content)
                res = await getProfit()
            except Exception as e:
                res = "error: {}".format(e)
            await  client.send_message(message.channel, res)
        elif message.content.startswith("!help") and message.author.name != client.user.name:
            res = "!help - for all command available\n"
            res += "!send amount mailaddress - for creating a transaction in hirbi\n"
            res += "!profit - to check how much you will get for exchanging btc through hiribi\n"
            res += "!check transactionid  - to check the transaction on the site"
            await  client.send_message(message.channel, res)

    client.run(getToken())


if __name__ == '__main__':
    try:
        main(len(sys.argv), sys.argv)
    except KeyboardInterrupt:
        pass
