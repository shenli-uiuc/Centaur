CREATE TABLE users(
    id INT,
    screen_name VARCHAR(50),
    follower_num INT,
    location VARCHAR(50), 

    PRIMARY KEY (id),
    INDEX (screen_name)
    INDEX (location)
)ENGINE=MyISAM CHARACTER SET=binary;
