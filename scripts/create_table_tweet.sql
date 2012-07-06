CREATE TABLE tweet(
    tweet_id BIGINT,
    user_id BIGINT,
    created_at VARCHAR(50),
    text VARCHAR(200),
    retweet_count BIGINT,
    retweeted BOOLEAN,
    pull_at BIGINT,

    PRIMARY KEY (tweet_id),
    INDEX (user_id),
    INDEX (created_at),
    INDEX (retweet_count),
    INDEX (retweeted),
    INDEX (pull_at)
)ENGINE=MyISAM CHARACTER SET=binary;
