CREATE TABLE internal_links(
    followee_id BIGINT,
    follower_id BIGINT,

    PRIMARY KEY (followee_id, follower_id),
    INDEX (followee_id),
    INDEX (follower_id)
)ENGINE=MyISAM CHARACTER SET=binary;
