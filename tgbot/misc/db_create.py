
from tgbot.misc.config import config



def db_create(conn):
    conn.cursor.execute("""
        CREATE TABLE pictures (
            id             INTEGER  PRIMARY KEY AUTOINCREMENT,
            pictures_code  STRING   UNIQUE,
            date           DATETIME DEFAULT (DATETIME('now', 'localtime') ),
            user_create_id INTEGER
        );""")
    conn.cursor.execute("""CREATE TABLE test (
            id               INTEGER  PRIMARY KEY AUTOINCREMENT,
            title            STRING,
            user_create_id   INTEGER  NOT NULL,
            test_code        STRING   UNIQUE
                                        NOT NULL,
            time_question    INTEGER  NOT NULL,
            random_mode      BOOLEAN,
            number_attempts  INTEGER,
            number_questions INTEGER,
            mark_3           INTEGER,
            mark_4           INTEGER,
            mark_5           INTEGER,
            active_mode      BOOLEAN  DEFAULT (0),
            date_create      DATETIME NOT NULL
                                        DEFAULT (DATETIME('now', 'localtime') ) 
        );""")
    conn.cursor.execute("""CREATE TABLE users (
            id                INTEGER  PRIMARY KEY AUTOINCREMENT,
            user_id           INTEGER  UNIQUE
                                        NOT NULL,
            join_date         DATETIME NOT NULL
                                        DEFAULT ( (DATETIME('now', 'localtime') ) ),
            user_name         STRING   NOT NULL,
            user_group        TEXT     NOT NULL,
            number_of_changes INTEGER  DEFAULT (0) 
        );""")
    conn.cursor.execute("""CREATE TABLE test_result (
            id      INTEGER  PRIMARY KEY AUTOINCREMENT
                                UNIQUE,
            user_id INTEGER  REFERENCES users (id) ON DELETE CASCADE
                                                    ON UPDATE CASCADE
                                NOT NULL,
            test_id INTEGER  REFERENCES test (id) ON DELETE CASCADE
                                                    ON UPDATE CASCADE,
            result  STRING,
            mark    STRING,
            data    DATETIME DEFAULT (DATETIME('now', 'localtime') ) 
                                NOT NULL
        );""")
    conn.cursor.execute("""CREATE TABLE question_result (
            id              INTEGER NOT NULL
                                    UNIQUE
                                    PRIMARY KEY AUTOINCREMENT,
            fk_id           INTEGER NOT NULL
                                    REFERENCES test_result (id) ON DELETE CASCADE
                                                                ON UPDATE CASCADE,
            result_question BOOLEAN,
            id_question     INTEGER,
            id_answer       INTEGER,
            text_response   STRING
        );""")
    conn.cursor.execute("""CREATE TABLE teachers (
            id                     INTEGER  PRIMARY KEY AUTOINCREMENT,
            name                   STRING,
            user_id                INTEGER,
            password_registration  STRING   DEFAULT (0),
            date_creative_password DATETIME DEFAULT (0),
            referral               INTEGER  DEFAULT NULL
        );""")
    conn.cursor.execute("""CREATE TABLE test_question (
            id          INTEGER PRIMARY KEY AUTOINCREMENT
                                UNIQUE
                                NOT NULL,
            fk_id       INTEGER NOT NULL
                                REFERENCES test (id) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
            question    STRING  NOT NULL,
            pictures_id STRING  DEFAULT NULL,
            time        INTEGER DEFAULT (0) 
        );""")
    conn.cursor.execute("""CREATE TABLE test_answer (
            id           INTEGER PRIMARY KEY AUTOINCREMENT
                                    NOT NULL,
            fk_id        INTEGER REFERENCES test_question (id) ON DELETE CASCADE
                                                                ON UPDATE CASCADE,
            answer       STRING,
            right_answer BOOLEAN NOT NULL
        );""")
    for c in config.tg_bot.admin_ids:
        conn.cursor.execute("INSERT INTO 'teachers' ('name','user_id') VALUES (?, ?)",("Admin", c))
    conn.commit()