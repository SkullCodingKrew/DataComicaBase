-- MySQL Workbench Synchronization
-- Generated: 2015-09-08 18:02
-- Model: test
-- Version: 1.0
-- Project: CDBase
-- Author: goaluix

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;

CREATE TABLE IF NOT EXISTS `mydb`.`comic` (
  `idcomic` INT(11) NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL DEFAULT NULL COMMENT '',
  `volume` INT(11) NULL DEFAULT NULL COMMENT '',
  `number` INT(11) NULL DEFAULT NULL COMMENT '',
  `title` VARCHAR(45) NULL DEFAULT NULL COMMENT '',
  `order_n` INT(11) NULL DEFAULT NULL COMMENT '',
  `cover_date` DATE NULL DEFAULT NULL COMMENT '',
  `release_date` DATE NULL DEFAULT NULL COMMENT '',
  `pages` INT(11) NULL DEFAULT NULL COMMENT '',
  `cover_price` DOUBLE NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idcomic`)  COMMENT '')
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `mydb`.`character` (
  `idcharacter` INT(11) NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idcharacter`)  COMMENT '')
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `mydb`.`artist` (
  `idartist` INT(11) NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL DEFAULT NULL COMMENT '',
  `type` INT(11) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idartist`)  COMMENT '',
  INDEX `id_artist_type_idx` (`type` ASC)  COMMENT '',
  CONSTRAINT `id_artist_type`
    FOREIGN KEY (`type`)
    REFERENCES `mydb`.`artist_type` (`idartist_type`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `mydb`.`artist_type` (
  `idartist_type` INT(11) NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idartist_type`)  COMMENT '')
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `mydb`.`story_arc` (
  `idstory_arc` INT(11) NOT NULL COMMENT '',
  `name` VARCHAR(45) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idstory_arc`)  COMMENT '')
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `mydb`.`comic-artist` (
  `idcomic-artist` INT(11) NOT NULL COMMENT '',
  `idcomic` INT(11) NULL DEFAULT NULL COMMENT '',
  `idartist` INT(11) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idcomic-artist`)  COMMENT '',
  INDEX `id_comic_idx` (`idcomic` ASC)  COMMENT '',
  INDEX `id_artist_idx` (`idartist` ASC)  COMMENT '',
  CONSTRAINT `id_comic`
    FOREIGN KEY (`idcomic`)
    REFERENCES `mydb`.`comic` (`idcomic`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id_artist`
    FOREIGN KEY (`idartist`)
    REFERENCES `mydb`.`artist` (`idartist`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

CREATE TABLE IF NOT EXISTS `mydb`.`comic-character` (
  `idcomic-character` INT(11) NOT NULL COMMENT '',
  `idcomic` INT(11) NULL DEFAULT NULL COMMENT '',
  `idcharacter` INT(11) NULL DEFAULT NULL COMMENT '',
  PRIMARY KEY (`idcomic-character`)  COMMENT '',
  INDEX `idcomic_idx` (`idcomic` ASC)  COMMENT '',
  INDEX `idcharacter_idx` (`idcharacter` ASC)  COMMENT '',
  CONSTRAINT `idcomic`
    FOREIGN KEY (`idcomic`)
    REFERENCES `mydb`.`comic` (`idcomic`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idcharacter`
    FOREIGN KEY (`idcharacter`)
    REFERENCES `mydb`.`character` (`idcharacter`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
