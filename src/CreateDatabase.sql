--SQL Table columns.
 -----> id (using to avoid duplicated tweets)
 -----> created_at (creation date of tweet)
 -----> text (tweet content)
 -----> verified (author.verified field to know if tweet ()
 -----> username (author.screen_name field who wrote tweet)
 -----> political_party (to join tweet with any political party)

CREATE DATABASE Political_forecast;
USE Political_forecast;
CREATE TABLE Tweets (
    id bigint NOT NULL PRIMARY KEY,
    created_at datetime NOT NULL,
    text varchar(500) NOT NULL,
    username varchar(15) NOT NULL,
    verified bit NOT NULL,
    political_party varchar(5) NOT NULL   
);