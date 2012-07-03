CREATE TABLE peer_id(
    id VARCHAR(100),
    ip VARCHAR(50), 

    PRIMARY KEY (id),
    INDEX (ip)
)ENGINE=MyISAM CHARACTER SET=binary;
