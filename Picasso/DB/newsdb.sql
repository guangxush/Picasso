CREATE TABLE `newsdb`.`user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` varchar(20) NOT NULL,
  `userinfo` varchar(255) NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `newsdb`.`news`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `newsid` varchar(20) NULL,
  `title` varchar(255) NULL,
  `category` int(11) NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `newsdb`.`user_news`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL,
  `newsid` int(11) NULL,
  `starttime` datetime(0) NULL,
  `endtime` datetime(0) NULL,
  `likes` int(1) NULL,
  `comments` varchar(255) NULL,
  PRIMARY KEY (`id`)
);