CREATE TABLE msg_log(
    timestamp BIGINT,
    msg_id BIGINT,
    receiver_id VARCHAR(128), 

    PRIMARY KEY (timestamp),
    INDEX (msg_id),
    INDEX (receiver_id)
)ENGINE=MyISAM CHARACTER SET=binary;
