CREATE TABLE ip_loc(
    ip VARCHAR(50),
    latitude DOUBLE,
    longitude DOUBLE,

    PRIMARY KEY (ip),
    INDEX (latitude),
    INDEX (longitude)
)ENGINE=MyISAM CHARACTER SET=binary;
