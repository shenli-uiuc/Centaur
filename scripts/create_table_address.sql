CREATE TABLE address(
    location VARCHAR(50),
    latitude DOUBLE,
    longitude DOUBLE,

    PRIMARY KEY (location),
    INDEX (latitude),
    INDEX (longitude)
)ENGINE=MyISAM CHARACTER SET=binary;
