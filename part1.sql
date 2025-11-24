SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS appointment;
DROP TABLE IF EXISTS job_application;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS address;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS caregivers;
DROP TABLE IF EXISTS users;

SET FOREIGN_KEY_CHECKS = 1;

-- 1) Users
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  given_name VARCHAR(100) NOT NULL,
  surname VARCHAR(100) NOT NULL,
  city VARCHAR(100) NOT NULL,
  phone_number VARCHAR(30),
  profile_description TEXT,
  password VARCHAR(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2) Caregivers
CREATE TABLE caregivers (
  caregiver_user_id INT NOT NULL,
  photo VARCHAR(255),
  gender VARCHAR(20),
  caregiving_type ENUM('babysitter','elderly_care','playmate','supertype') NOT NULL,
  hourly_rate DECIMAL(6,2) NOT NULL CHECK (hourly_rate >= 0),
  PRIMARY KEY (caregiver_user_id),
  CONSTRAINT fk_caregivers_users FOREIGN KEY (caregiver_user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3) Members
CREATE TABLE members (
  member_user_id INT NOT NULL,
  house_rules TEXT,
  dependent_description TEXT,
  PRIMARY KEY (member_user_id),
  CONSTRAINT fk_members_users FOREIGN KEY (member_user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4) Address 
CREATE TABLE address (
  member_user_id INT NOT NULL,
  house_number VARCHAR(20),
  street VARCHAR(200),
  town VARCHAR(100),
  PRIMARY KEY (member_user_id),
  CONSTRAINT fk_address_members FOREIGN KEY (member_user_id) REFERENCES members(member_user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5) Job postings
CREATE TABLE job (
  job_id INT AUTO_INCREMENT PRIMARY KEY,
  member_user_id INT NOT NULL,
  required_caregiving_type ENUM('babysitter','elderly_care','playmate','supertype') NOT NULL,
  other_requirements TEXT,
  person_age INT,
  time_interval VARCHAR(100),
  frequency VARCHAR(100),
  date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_job_members FOREIGN KEY (member_user_id) REFERENCES members(member_user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6) Job applications
CREATE TABLE job_application (
  caregiver_user_id INT NOT NULL,
  job_id INT NOT NULL,
  date_applied TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (caregiver_user_id, job_id),
  CONSTRAINT fk_ja_caregivers FOREIGN KEY (caregiver_user_id) REFERENCES caregivers(caregiver_user_id) ON DELETE CASCADE,
  CONSTRAINT fk_ja_job FOREIGN KEY (job_id) REFERENCES job(job_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7) Appointments
CREATE TABLE appointment (
  appointment_id INT AUTO_INCREMENT PRIMARY KEY,
  caregiver_user_id INT NOT NULL,
  member_user_id INT NOT NULL,
  appointment_date DATE NOT NULL,
  appointment_time TIME NOT NULL,
  work_hours INT NOT NULL CHECK (work_hours > 0),
  status ENUM('pending','confirmed','declined') NOT NULL DEFAULT 'pending',
  CONSTRAINT fk_app_caregiver FOREIGN KEY (caregiver_user_id) REFERENCES caregivers(caregiver_user_id) ON DELETE CASCADE,
  CONSTRAINT fk_app_member FOREIGN KEY (member_user_id) REFERENCES members(member_user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- USERS
INSERT INTO users (email,given_name,surname,city,phone_number,profile_description,password) VALUES
('arman@example.com','Arman','Armanov','Astana','+77770000001','Experienced caregiver','pass123'),
('amina@example.com','Amina','Aminova','Almaty','+77001112233','Looking for part-time help','pass123'),
('dina@example.com','Dina','Ibragim','Astana','+77001112234','Friendly neighbour','pass123'),
('zhanar@example.com','Zhanar','Ospan','Astana','+77001112235','Has elderly father','pass123'),
('gulzhan@example.com','Gulzhan','Sadykova','Almaty','+77001112236','Loves kids','pass123'),
('serik@example.com','Serik','Kairat','Astana','+77001112237','Reliable and punctual','pass123'),
('aliya@example.com','Aliya','Nurlan','Shymkent','+77001112238','Interested in babysitting','pass123'),
('marat@example.com','Marat','Bek','Astana','+77001112239','Experienced nurse assistant','pass123'),
('arman2@example.com','Arman','Suleimen','Astana','+77001112240','Part-time caregiver','pass123'),
('nurgul@example.com','Nurgul','Tulegen','Astana','+77001112241','Prefers short shifts','pass123'),
('amina2@example.com','Amina','K','Kokshetau','+77001112242','Posting jobs often','pass123'),
('stepan@example.com','Stepan','Ivanov','Astana','+77001112243','Willing to travel','pass123');

-- CAREGIVERS
INSERT INTO caregivers (caregiver_user_id,photo,gender,caregiving_type,hourly_rate) VALUES
(1,'/photos/arman.jpg','male','babysitter',8.50),
(3,'/photos/dina.jpg','female','playmate',6.00),
(5,'/photos/gulzhan.jpg','female','babysitter',12.00),
(6,'/photos/serik.jpg','male','elderly_care',15.00),
(7,'/photos/aliya.jpg','female','babysitter',9.50),
(8,'/photos/marat.jpg','male','elderly_care',11.00),
(9,'/photos/arman2.jpg','male','elderly_care',7.50),
(10,'/photos/nurgul.jpg','female','playmate',5.00),
(2,'/photos/amina_cg.jpg','female','babysitter',9.00),
(11,'/photos/amina2_cg.jpg','female','elderly_care',8.75);

-- MEMBERS
INSERT INTO members (member_user_id,house_rules,dependent_description) VALUES
(2,'No smoking. No pets.','I have a 72-year-old mother with mild dementia.'),
(4,'No pets. Respect sleep hours.','Looking after 3-year-old daughter.'),
(12,'No pets.','Require short-term care for recovery after surgery.'),
(1,'No shoes inside. No pets.','I need a babysitter for my 5-year-old son.'),
(11,'No pets. Soft voice preferred.','Elderly father, 80 years old.'),
(5,'No pets. No loud music.','Baby, needs feeding and nap supervision.'),
(3,'No pets.','Student needs occasional supervision.'),
(6,'No pets.','Elderly care needed on weekends only.'),
(7,'No pets.','Playmate for 4-year-old twins.'),
(9,'No smoking. No pets.','One toddler who likes reading.');

-- ADDRESS
INSERT INTO address (member_user_id,house_number,street,town) VALUES
(2,'12A','Kabanbay Batyr','Astana'),
(4,'5','Tauelsizdik Ave','Astana'),
(12,'22','Kabanbay Batyr','Astana'),
(1,'11','Pushkin St','Astana'),
(11,'9','Orken St','Kokshetau'),
(5,'3','Kultoba St','Almaty'),
(3,'44','Kabanbay Batyr','Astana'),
(6,'7','Abylay Khan Ave','Astana'),
(7,'2','Auezov St','Shymkent'),
(9,'88','Kabanbay Batyr','Astana');

-- JOB
INSERT INTO job (member_user_id,required_caregiving_type,other_requirements,date_posted) VALUES
(2,'elderly_care','soft-spoken, experience with dementia, valid certificate',CURRENT_TIMESTAMP - INTERVAL 20 DAY),
(4,'babysitter','experience with toddlers, CPR certified',CURRENT_TIMESTAMP - INTERVAL 10 DAY),
(12,'babysitter','no allergies, soft-spoken preferred',CURRENT_TIMESTAMP - INTERVAL 9 DAY),
(1,'babysitter','playful, likes painting, available 09:00-12:00',CURRENT_TIMESTAMP - INTERVAL 5 DAY),
(11,'elderly_care','no pets, soft-spoken, weekends only',CURRENT_TIMESTAMP - INTERVAL 4 DAY),
(5,'babysitter','must help with feeding and nap schedule',CURRENT_TIMESTAMP - INTERVAL 15 DAY),
(3,'playmate','energetic, must play outdoors',CURRENT_TIMESTAMP - INTERVAL 3 DAY),
(6,'elderly_care','overnight experience preferred',CURRENT_TIMESTAMP - INTERVAL 2 DAY),
(7,'babysitter','twins experience required',CURRENT_TIMESTAMP - INTERVAL 1 DAY),
(9,'elderly_care','patient, no loud music',CURRENT_TIMESTAMP - INTERVAL 7 DAY);

-- JOB_APPLICATION: create several applications, multiple applicants per job
INSERT INTO job_application (caregiver_user_id,job_id,date_applied) VALUES
(1,2,CURRENT_TIMESTAMP - INTERVAL 9 DAY),
(5,2,CURRENT_TIMESTAMP - INTERVAL 8 DAY),
(7,4,CURRENT_TIMESTAMP - INTERVAL 4 DAY),
(3,1,CURRENT_TIMESTAMP - INTERVAL 18 DAY),
(6,1,CURRENT_TIMESTAMP - INTERVAL 17 DAY),
(9,1,CURRENT_TIMESTAMP - INTERVAL 12 DAY),
(2,3,CURRENT_TIMESTAMP - INTERVAL 8 DAY),
(10,5,CURRENT_TIMESTAMP - INTERVAL 3 DAY),
(11,9,CURRENT_TIMESTAMP - INTERVAL 6 DAY),
(8,6,CURRENT_TIMESTAMP - INTERVAL 14 DAY),
(1,4,CURRENT_TIMESTAMP - INTERVAL 6 DAY);

-- APPOINTMENT
INSERT INTO appointment (caregiver_user_id,member_user_id,appointment_date,appointment_time,work_hours,status) VALUES
(1,1,'2025-11-10','09:00:00',3,'confirmed'),
(5,5,'2025-11-12','10:00:00',2,'pending'),
(6,2,'2025-11-08','08:00:00',4,'confirmed'),
(9,11,'2025-10-30','14:00:00',3,'declined'),
(2,4,'2025-11-15','12:00:00',5,'confirmed'),
(7,7,'2025-11-18','15:00:00',2,'confirmed'),
(3,3,'2025-11-20','09:00:00',3,'pending'),
(8,6,'2025-11-05','08:00:00',6,'confirmed'),
(10,9,'2025-11-22','11:00:00',1,'confirmed'),
(11,12,'2025-11-02','10:00:00',2,'confirmed');
