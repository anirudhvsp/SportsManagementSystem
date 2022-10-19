-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`players`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`players` (
  `playerId` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `gender` VARCHAR(45) NULL,
  `sport` INT NULL,
  `age` INT NULL,
  `email` VARCHAR(45) NULL,
  PRIMARY KEY (`playerId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`sports`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`sports` (
  `sportId` INT NOT NULL AUTO_INCREMENT,
  `sportName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`sportId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`player_sport_mapping`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`player_sport_mapping` (
  `playerId` INT NULL,
  `sportId` INT NULL,
  `psMappingId` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`psMappingId`),
  INDEX `fk_player_sport_mapping_players_idx` (`playerId` ASC) VISIBLE,
  INDEX `fk_player_sport_mapping_sports1_idx` (`sportId` ASC) VISIBLE,
  CONSTRAINT `fk_player_sport_mapping_players`
    FOREIGN KEY (`playerId`)
    REFERENCES `mydb`.`players` (`playerId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_player_sport_mapping_sports1`
    FOREIGN KEY (`sportId`)
    REFERENCES `mydb`.`sports` (`sportId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`credentials`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`credentials` (
  `playerId` INT NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `isAdmin` INT NOT NULL,
  UNIQUE INDEX `playerId_UNIQUE` (`playerId` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `password_UNIQUE` (`password` ASC) VISIBLE,
  CONSTRAINT `fk_credentials_players1`
    FOREIGN KEY (`playerId`)
    REFERENCES `mydb`.`players` (`playerId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`teams`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`teams` (
  `teamId` INT NOT NULL AUTO_INCREMENT,
  `teamName` VARCHAR(45) NULL,
  `sportId` INT NULL,
  `captainId` INT NULL,
  PRIMARY KEY (`teamId`),
  INDEX `fk_teams_sports1_idx` (`sportId` ASC) VISIBLE,
  INDEX `fk_teams_players1_idx` (`captainId` ASC) VISIBLE,
  CONSTRAINT `fk_teams_sports1`
    FOREIGN KEY (`sportId`)
    REFERENCES `mydb`.`sports` (`sportId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_teams_players1`
    FOREIGN KEY (`captainId`)
    REFERENCES `mydb`.`players` (`playerId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tournaments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tournaments` (
  `tournamentId` INT NOT NULL AUTO_INCREMENT,
  `tournamentName` VARCHAR(45) NULL,
  `tournamentDescription` VARCHAR(45) NULL,
  `sportId` INT NULL,
  PRIMARY KEY (`tournamentId`),
  INDEX `fk_tournaments_sports1_idx` (`sportId` ASC) VISIBLE,
  CONSTRAINT `fk_tournaments_sports1`
    FOREIGN KEY (`sportId`)
    REFERENCES `mydb`.`sports` (`sportId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`tournament_team_mapping`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`tournament_team_mapping` (
  `tournamentId` INT NULL,
  `teamId` INT NULL,
  `ttMappingId` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ttMappingId`),
  INDEX `fk_tournament_team_mapping_tournaments1_idx` (`tournamentId` ASC) VISIBLE,
  INDEX `fk_tournament_team_mapping_teams1_idx` (`teamId` ASC) VISIBLE,
  CONSTRAINT `fk_tournament_team_mapping_tournaments1`
    FOREIGN KEY (`tournamentId`)
    REFERENCES `mydb`.`tournaments` (`tournamentId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_tournament_team_mapping_teams1`
    FOREIGN KEY (`teamId`)
    REFERENCES `mydb`.`teams` (`teamId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`player_team_mapping`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`player_team_mapping` (
  `playerId` INT NULL,
  `teamId` INT NULL,
  `ptMappingId` INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`ptMappingId`),
  INDEX `fk_player_team_mapping_players1_idx` (`playerId` ASC) VISIBLE,
  INDEX `fk_player_team_mapping_teams1_idx` (`teamId` ASC) VISIBLE,
  CONSTRAINT `fk_player_team_mapping_players1`
    FOREIGN KEY (`playerId`)
    REFERENCES `mydb`.`players` (`playerId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_player_team_mapping_teams1`
    FOREIGN KEY (`teamId`)
    REFERENCES `mydb`.`teams` (`teamId`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
  ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
