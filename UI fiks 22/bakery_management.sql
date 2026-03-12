/*
SQLyog Community v13.3.0 (64 bit)
MySQL - 10.4.32-MariaDB : Database - bakery_management
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`bakery_management` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `bakery_management`;

/*Table structure for table `absensi` */

DROP TABLE IF EXISTS `absensi`;

CREATE TABLE `absensi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `karyawan_id` int(11) DEFAULT NULL,
  `tanggal` date DEFAULT NULL,
  `waktu_masuk` time DEFAULT NULL,
  `waktu_pulang` time DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `karyawan_id` (`karyawan_id`),
  CONSTRAINT `absensi_ibfk_1` FOREIGN KEY (`karyawan_id`) REFERENCES `karyawan` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `absensi` */

insert  into `absensi`(`id`,`karyawan_id`,`tanggal`,`waktu_masuk`,`waktu_pulang`,`status`) values 
(1,2,'2025-12-17','10:31:51','10:32:22','Hadir'),
(2,2,'2025-01-01',NULL,NULL,'Cuti');

/*Table structure for table `cuti` */

DROP TABLE IF EXISTS `cuti`;

CREATE TABLE `cuti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `karyawan_id` int(11) DEFAULT NULL,
  `tanggal_mulai` date DEFAULT NULL,
  `jumlah_hari` int(11) DEFAULT NULL,
  `alasan` text DEFAULT NULL,
  `status_validasi` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  KEY `karyawan_id` (`karyawan_id`),
  CONSTRAINT `cuti_ibfk_1` FOREIGN KEY (`karyawan_id`) REFERENCES `karyawan` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `cuti` */

insert  into `cuti`(`id`,`karyawan_id`,`tanggal_mulai`,`jumlah_hari`,`alasan`,`status_validasi`) values 
(1,2,'2025-01-01',1,'Sakit','Disetujui');

/*Table structure for table `gaji` */

DROP TABLE IF EXISTS `gaji`;

CREATE TABLE `gaji` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `karyawan_id` int(11) DEFAULT NULL,
  `bulan` int(11) DEFAULT NULL,
  `tahun` int(11) DEFAULT NULL,
  `gaji_pokok` double DEFAULT NULL,
  `total_tunjangan` double DEFAULT NULL,
  `total_potongan` double DEFAULT NULL,
  `total_gaji` double DEFAULT NULL,
  `status_transfer` varchar(20) DEFAULT 'Pending',
  `tanggal_transfer` date DEFAULT NULL,
  `bukti_transfer` varchar(255) DEFAULT NULL,
  `status_validasi` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`id`),
  KEY `karyawan_id` (`karyawan_id`),
  CONSTRAINT `gaji_ibfk_1` FOREIGN KEY (`karyawan_id`) REFERENCES `karyawan` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `gaji` */

insert  into `gaji`(`id`,`karyawan_id`,`bulan`,`tahun`,`gaji_pokok`,`total_tunjangan`,`total_potongan`,`total_gaji`,`status_transfer`,`tanggal_transfer`,`bukti_transfer`,`status_validasi`) values 
(1,1,12,2025,4000000,500000,4000000,500000,'Pending',NULL,NULL,'Pending'),
(2,2,12,2025,3000000,250000,2884615.384615385,365384.615384615,'Pending',NULL,NULL,'Valid'),
(3,1,12,2023,4000000,500000,4000000,500000,'Pending',NULL,NULL,'Pending'),
(4,2,12,2023,3000000,250000,3000000,250000,'Pending',NULL,NULL,'Pending'),
(5,1,12,2026,4000000,500000,4000000,500000,'Pending',NULL,NULL,'Pending'),
(6,2,12,2026,3000000,250000,3000000,250000,'Pending',NULL,NULL,'Pending');

/*Table structure for table `jabatan` */

DROP TABLE IF EXISTS `jabatan`;

CREATE TABLE `jabatan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_jabatan` varchar(50) NOT NULL,
  `gaji_pokok` double NOT NULL,
  `tunjangan_jabatan` double NOT NULL,
  `tunjangan_kehadiran` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nama_jabatan` (`nama_jabatan`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `jabatan` */

insert  into `jabatan`(`id`,`nama_jabatan`,`gaji_pokok`,`tunjangan_jabatan`,`tunjangan_kehadiran`) values 
(1,'Admin',4000000,500000,200000),
(2,'Kasir',3000000,250000,150000),
(3,'Baker',3500000,300000,150000);

/*Table structure for table `karyawan` */

DROP TABLE IF EXISTS `karyawan`;

CREATE TABLE `karyawan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_lengkap` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `jabatan` varchar(50) NOT NULL,
  `status_kerja` varchar(20) NOT NULL,
  `status_akun` varchar(20) DEFAULT 'Aktif',
  `tanggal_gabung` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `karyawan` */

insert  into `karyawan`(`id`,`nama_lengkap`,`email`,`password`,`jabatan`,`status_kerja`,`status_akun`,`tanggal_gabung`) values 
(1,'Super Admin','admin@toko.com','admin123','Admin','Tetap','Aktif','2025-12-17'),
(2,'Sinta Andini','sinta@toko.com','sinta123','Kasir','Kontrak','Aktif','2025-12-17');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
