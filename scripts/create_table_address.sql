CREATE TABLE address(
    location VARCHAR(50),
    latitude DOUBLE,
    longitude DOUBLE,
    formatted_address VARCHAR(200),
    types VARCHAR(30),

    PRIMARY KEY (location),
    INDEX (latitude),
    INDEX (longitude),
    INDEX (types)
)ENGINE=MyISAM CHARACTER SET=binary;
