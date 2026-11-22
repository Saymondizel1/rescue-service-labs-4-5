USE `lab1`;

-- 1. Додаткова таблиця (зв'язок 1:M з cities) + тригери замість FK
CREATE TABLE IF NOT EXISTS `lab1`.`city_districts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `Cities_id` INT NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB;

DELIMITER //

CREATE TRIGGER trg_city_districts_before_insert
BEFORE INSERT ON `lab1`.`city_districts`
FOR EACH ROW
BEGIN
    DECLARE city_exists INT;
    SELECT COUNT(*) INTO city_exists FROM `lab1`.`cities` WHERE id = NEW.Cities_id;
    IF city_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Помилка цілісності: вказаного міста (Cities_id) не існує!';
    END IF;
END //

CREATE TRIGGER trg_city_districts_before_update
BEFORE UPDATE ON `lab1`.`city_districts`
FOR EACH ROW
BEGIN
    DECLARE city_exists INT;
    SELECT COUNT(*) INTO city_exists FROM `lab1`.`cities` WHERE id = NEW.Cities_id;
    IF city_exists = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Помилка цілісності: вказаного міста (Cities_id) не існує!';
    END IF;
END //

-- 2. Збережені процедури, функція та курсор
CREATE PROCEDURE sp_insert_city(IN p_name VARCHAR(100))
BEGIN
    INSERT INTO `lab1`.`cities` (`name`) VALUES (p_name);
END //

CREATE PROCEDURE sp_link_vehicle_equipment(
    IN p_vehicle_brand VARCHAR(100),
    IN p_equipment_name VARCHAR(100)
)
BEGIN
    DECLARE v_veh_id INT;
    DECLARE v_eq_id INT;
    
    SELECT id INTO v_veh_id FROM `lab1`.`vehicles` WHERE brand = p_vehicle_brand LIMIT 1;
    SELECT id INTO v_eq_id FROM `lab1`.`equipments` WHERE name = p_equipment_name LIMIT 1;
    
    IF v_veh_id IS NOT NULL AND v_eq_id IS NOT NULL THEN
        INSERT IGNORE INTO `lab1`.`vehicles_has_equipments` (`vehicles_id`, `equipments_id`)
        VALUES (v_veh_id, v_eq_id);
    ELSE
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Транспорт або спорядження з такою назвою не знайдено!';
    END IF;
END //

CREATE PROCEDURE sp_insert_10_cities()
BEGIN
    DECLARE i INT DEFAULT 1;
    WHILE i <= 10 DO
        INSERT INTO `lab1`.`cities` (`name`) VALUES (CONCAT('Noname', i));
        SET i = i + 1;
    END WHILE;
END //

CREATE FUNCTION fn_get_avg_rescuers_per_call()
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_avg DECIMAL(10,2);
    SELECT AVG(rescuer_count) INTO v_avg
    FROM (
        SELECT COUNT(rescuers_id) AS rescuer_count
        FROM `lab1`.`call_rescuers`
        GROUP BY calls_id
    ) AS t;
    RETURN IFNULL(v_avg, 0.0);
END //

CREATE PROCEDURE sp_get_avg_rescuers()
BEGIN
    SELECT fn_get_avg_rescuers_per_call() AS 'Average_Rescuers_Per_Call';
END //

CREATE PROCEDURE sp_split_cities_randomly()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_id INT;
    DECLARE v_name VARCHAR(100);
    DECLARE t_name1 VARCHAR(100);
    DECLARE t_name2 VARCHAR(100);

    DECLARE city_cursor CURSOR FOR SELECT id, name FROM `lab1`.`cities`;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    SET t_name1 = CONCAT('cities_part1_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'));
    SET t_name2 = CONCAT('cities_part2_', DATE_FORMAT(NOW(), '%Y%m%d_%H%i%s'));

    SET @q1 = CONCAT('CREATE TABLE ', t_name1, ' LIKE `lab1`.`cities`');
    PREPARE stmt1 FROM @q1; EXECUTE stmt1; DEALLOCATE PREPARE stmt1;
    
    SET @q2 = CONCAT('CREATE TABLE ', t_name2, ' LIKE `lab1`.`cities`');
    PREPARE stmt2 FROM @q2; EXECUTE stmt2; DEALLOCATE PREPARE stmt2;
    
    OPEN city_cursor;
    read_loop: LOOP
        FETCH city_cursor INTO v_id, v_name;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        IF RAND() > 0.5 THEN
            SET @ins = CONCAT('INSERT INTO ', t_name1, ' (id, name) VALUES (?, ?)');
        ELSE
            SET @ins = CONCAT('INSERT INTO ', t_name2, ' (id, name) VALUES (?, ?)');
        END IF;
        
        SET @v1 = v_id; 
        SET @v2 = v_name;
        PREPARE stmt_ins FROM @ins;
        EXECUTE stmt_ins USING @v1, @v2;
        DEALLOCATE PREPARE stmt_ins;
    END LOOP;
    
    CLOSE city_cursor;
END //

-- 3. Додаткові тригери бізнес-логіки та журналювання
CREATE TRIGGER trg_prevent_update_emergency_types
BEFORE UPDATE ON `lab1`.`emergency_types`
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Помилка: Оновлення типів надзвичайних ситуацій заборонено!';
END //

CREATE TRIGGER trg_prevent_delete_calls
BEFORE DELETE ON `lab1`.`calls`
FOR EACH ROW
BEGIN
    SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Помилка: Видаляти записи про екстрені виклики заборонено правилами безпеки!';
END //

DELIMITER ;

CREATE TABLE IF NOT EXISTS `lab1`.`rescuers_audit_log` (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    deleted_rescuer_id INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    deleted_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

DELIMITER //

CREATE TRIGGER trg_log_rescuer_delete
AFTER DELETE ON `lab1`.`rescuers`
FOR EACH ROW
BEGIN
    INSERT INTO `lab1`.`rescuers_audit_log` (deleted_rescuer_id, first_name, last_name)
    VALUES (OLD.id, OLD.first_name, OLD.last_name);
END //

DELIMITER ;