from fastapi import FastAPI
from starlette.responses import StreamingResponse
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt


app = FastAPI()

@app.get("/forumData")

def forumData():
    db = mysql.connector.connect(
        host="ocu-cs-mysql.mysql.database.azure.com",
        port="3306",
        user="campusmap",
        password="BestMapEver$123",
        database="capstone_campusmap"
    )

    cursor = db.cursor()

    cursor.execute(
        "SELECT Tag, COUNT(`solved?`), `Date Posted` from forumdata where `solved?` = 1 group by Tag, `Date Posted`")

    solved = cursor.fetchall()

    cursor.execute(
        "SELECT Tag, COUNT(`solved?`), `Date Posted` from forumdata where `solved?` = 0 group by Tag, `Date Posted`")

    failed = cursor.fetchall()

    df1 = pd.DataFrame(solved, columns=['tag', 'solved', 'date'])
    df2 = pd.DataFrame(failed, columns=['tag', 'failed', 'date'])
    data = pd.concat([df1, df2])

    data.set_index('date')
    data['solved'] = data['solved'].fillna(0)
    data['failed'] = data['failed'].fillna(0)

    ax = data.plot.bar(x='date', y=['solved', 'failed'])

    plt.show()

    plt.savefig('data.png')
    file = open('data.png', mode="rb")

    return StreamingResponse(file, media_type="image/png")
