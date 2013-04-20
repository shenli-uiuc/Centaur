CREATE TABLE user_status(
    time BIGINT,
    user_id VARCHAR(128),
    ip VARCHAR(70),
    addr VARCHAR(70),
    latitude DOUBLE,
    longitude DOUBLE, 

    PRIMARY KEY (time),
    INDEX (user_id)
)ENGINE=MyISAM CHARACTER SET=binary;
