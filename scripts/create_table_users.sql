CREATE TABLE users_complete(
    id BIGINT,
    screen_name VARCHAR(50),
    follower_count BIGINT,
    friend_count BIGINT,
    status_count BIGINT,
    favor_count BIGINT,
    verified BOOLEAN,
    created_at VARCHAR(50),
    location VARCHAR(50), 

    PRIMARY KEY (id),
    INDEX (screen_name),
    INDEX (location),
    INDEX (follower_count),
    INDEX (friend_COUNT),
    INDEX (status_count),
    INDEX (verified),
    INDEX (favor_count)
)ENGINE=MyISAM CHARACTER SET=binary;
