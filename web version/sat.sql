-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2013 年 10 月 11 日 16:21
-- 服务器版本: 5.5.30-log
-- PHP 版本: 5.5.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `sat`
--
CREATE DATABASE IF NOT EXISTS `sat` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `sat`;

-- --------------------------------------------------------

--
-- 表的结构 `settings`
--

CREATE TABLE IF NOT EXISTS `settings` (
  `name` varchar(30) NOT NULL,
  `value` varchar(30) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `settings`
--

INSERT INTO `settings` (`name`, `value`) VALUES
('admin', 'junfeng7@qq.com');

-- --------------------------------------------------------

--
-- 表的结构 `tiebas`
--

CREATE TABLE IF NOT EXISTS `tiebas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tieba` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- 转存表中的数据 `tiebas`
--

INSERT INTO `tiebas` (`id`, `tieba`) VALUES
(4, 'pt');

-- --------------------------------------------------------

--
-- 表的结构 `tiebas_users`
--

CREATE TABLE IF NOT EXISTS `tiebas_users` (
  `tieba_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `tiebas_users`
--

INSERT INTO `tiebas_users` (`tieba_id`, `user_id`, `message`) VALUES
(4, 1, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `cookie` varchar(2000) DEFAULT NULL,
  `passwd` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=6 ;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`id`, `email`, `name`, `cookie`, `passwd`) VALUES
(1, 'junfeng7@qq.com', 'admin', 'SSUDB=k93OWs0ZWF4OTIyLTVsSTFTdXQzbnBaSEkyWlp-S3F2NFZtZUx3RmE5RTJNanRSQVFBQUFBJCQAAAAAAAAAAAEAAABFrHAcz6bEq9niAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADalE1E2pRNRR; bdshare_firstime=1360508402263; BDREFER=%7Burl%3A%22http%3A//news.baidu.com/%22%2Cword%3A%22%22%7D; BDUT=di484EE687493638CAD4ACFF14E30ED0A2A813cac5126101; interestSmiley=show; TIEBAUID=35f770fcd2202f0c3321083e; Hm_lvt_73dca03586694a616c988dcf7fa67e11=1360622332; TIEBA_USERTYPE=d7b21ecc21ae57be9d75d8bb; BAIDUID=8A3C16CB8188951D2337594F32906CA3:FG=1; SFSSID=bdb07acf7c3a2f8533fe496e4d489da8; BAIDU_WISE_UID=A61FBA804F386C31B2F570C336F12099; SIGNIN_UC=70a2711cf1d3d9b1a82d2f87d633bd8a01285375566; wise_device=0; Hm_lvt_287705c8d9e2073d13275b18dbd746dc=1377544869,1378751485,1379781205; Hm_lpvt_287705c8d9e2073d13275b18dbd746dc=1380047771; H_PS_PSSID=3407_3424_2776_1433_2976_2981_3417; MCITY=-179%3A; BDUSS=ndsc3BHRWlvNmQ4V3EwUE5mWlBPdjhUdFY5SFY4NTl4bDJyWnFmdmlnNGxlWGRTQVFBQUFBJCQAAAAAAAAAAAEAAABFrHAcz6bEq9niAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACXsT1Il7E9SW; cflag=65535%3A1', 'a1ce08382f1fc86d8ae4b3abd31a0b69'),
(5, 'junfeng17@gmail.com', 'user', NULL, '53e8254b3222a33f42b5a6b3d156056c');
