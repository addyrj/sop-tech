-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 07, 2026 at 11:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `clienttest`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add display tv', 7, 'add_displaytv'),
(26, 'Can change display tv', 7, 'change_displaytv'),
(27, 'Can delete display tv', 7, 'delete_displaytv'),
(28, 'Can view display tv', 7, 'view_displaytv'),
(29, 'Can add media bucket', 8, 'add_mediabucket'),
(30, 'Can change media bucket', 8, 'change_mediabucket'),
(31, 'Can delete media bucket', 8, 'delete_mediabucket'),
(32, 'Can view media bucket', 8, 'view_mediabucket'),
(33, 'Can add Media Content', 9, 'add_mediacontent'),
(34, 'Can change Media Content', 9, 'change_mediacontent'),
(35, 'Can delete Media Content', 9, 'delete_mediacontent'),
(36, 'Can view Media Content', 9, 'view_mediacontent'),
(37, 'Can add production line', 10, 'add_productionline'),
(38, 'Can change production line', 10, 'change_productionline'),
(39, 'Can delete production line', 10, 'delete_productionline'),
(40, 'Can view production line', 10, 'view_productionline'),
(41, 'Can add Volume Admin', 11, 'add_volumetv'),
(42, 'Can change Volume Admin', 11, 'change_volumetv'),
(43, 'Can delete Volume Admin', 11, 'delete_volumetv'),
(44, 'Can view Volume Admin', 11, 'view_volumetv'),
(45, 'Can add StorageTV Admin', 12, 'add_storagetv'),
(46, 'Can change StorageTV Admin', 12, 'change_storagetv'),
(47, 'Can delete StorageTV Admin', 12, 'delete_storagetv'),
(48, 'Can view StorageTV Admin', 12, 'view_storagetv'),
(49, 'Can add StatusTV Admin', 13, 'add_statustv'),
(50, 'Can change StatusTV Admin', 13, 'change_statustv'),
(51, 'Can delete StatusTV Admin', 13, 'delete_statustv'),
(52, 'Can view StatusTV Admin', 13, 'view_statustv'),
(53, 'Can add production line tv', 14, 'add_productionlinetv'),
(54, 'Can change production line tv', 14, 'change_productionlinetv'),
(55, 'Can delete production line tv', 14, 'delete_productionlinetv'),
(56, 'Can view production line tv', 14, 'view_productionlinetv'),
(57, 'Can add Production Admin', 15, 'add_productionadmin'),
(58, 'Can change Production Admin', 15, 'change_productionadmin'),
(59, 'Can delete Production Admin', 15, 'delete_productionadmin'),
(60, 'Can view Production Admin', 15, 'view_productionadmin'),
(61, 'Can add media system', 16, 'add_mediasystem'),
(62, 'Can change media system', 16, 'change_mediasystem'),
(63, 'Can delete media system', 16, 'delete_mediasystem'),
(64, 'Can view media system', 16, 'view_mediasystem'),
(65, 'Can add media file', 17, 'add_mediafile'),
(66, 'Can change media file', 17, 'change_mediafile'),
(67, 'Can delete media file', 17, 'delete_mediafile'),
(68, 'Can view media file', 17, 'view_mediafile'),
(69, 'Can add Admin', 18, 'add_admin'),
(70, 'Can change Admin', 18, 'change_admin'),
(71, 'Can delete Admin', 18, 'delete_admin'),
(72, 'Can view Admin', 18, 'view_admin'),
(73, 'Can add client user map', 19, 'add_clientusermap'),
(74, 'Can change client user map', 19, 'change_clientusermap'),
(75, 'Can delete client user map', 19, 'delete_clientusermap'),
(76, 'Can view client user map', 19, 'view_clientusermap'),
(77, 'Can add machine runtime', 20, 'add_machineruntime'),
(78, 'Can change machine runtime', 20, 'change_machineruntime'),
(79, 'Can delete machine runtime', 20, 'delete_machineruntime'),
(80, 'Can view machine runtime', 20, 'view_machineruntime'),
(81, 'Can add client', 21, 'add_client'),
(82, 'Can change client', 21, 'change_client'),
(83, 'Can delete client', 21, 'delete_client'),
(84, 'Can view client', 21, 'view_client');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$J5jNTDIGBycXXTjc8KO13q$m6am4kgWV99KG38N2c+QggsZ90bEAYxUc146WNHS1dA=', NULL, 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2026-05-07 07:34:17.544993'),
(2, 'pbkdf2_sha256$600000$dLhHN37iXcZUHSgnyhVP6U$qKBNceOE/zacEa40QFVm/vneEd2psP4Hgg6i9XiwRsU=', NULL, 1, 'admins', '', '', 'admin@gmail.com', 1, 1, '2026-05-07 07:42:56.412067'),
(3, 'pbkdf2_sha256$600000$7LW777KuNl7HoHsUnWzhz5$2QWBb1+vyFKo8AGgTwG71wJ0yGY3Cus4gx7jlGuZnP8=', NULL, 1, 'iot', '', '', 'admin@gmail.com', 1, 1, '2026-05-07 07:53:59.822864'),
(4, 'pbkdf2_sha256$600000$fg9JcIiSe5wNGm7ZPPBteE$E30js5ItobChDfsDz9vP7B8zs9lN50A/60/BLbfPRGk=', NULL, 1, 'adminb', '', '', 'admin@gmail.com', 1, 1, '2026-05-07 08:20:42.829647'),
(5, 'pbkdf2_sha256$600000$cKeJwoDRN42kwg5pIo9NFv$7jluf9bDqnUG4kl4lSI7DGR/Vs5VwiGCGtzS2I9kCEw=', '2026-05-07 08:31:28.710351', 1, 'buts', '', '', 'buts@gmail.com', 1, 1, '2026-05-07 08:29:48.381652');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session'),
(18, 'sop', 'admin'),
(21, 'sop', 'client'),
(19, 'sop', 'clientusermap'),
(7, 'sop', 'displaytv'),
(20, 'sop', 'machineruntime'),
(8, 'sop', 'mediabucket'),
(9, 'sop', 'mediacontent'),
(17, 'sop', 'mediafile'),
(16, 'sop', 'mediasystem'),
(15, 'sop', 'productionadmin'),
(10, 'sop', 'productionline'),
(14, 'sop', 'productionlinetv'),
(13, 'sop', 'statustv'),
(12, 'sop', 'storagetv'),
(11, 'sop', 'volumetv');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2026-05-07 07:33:50.250027'),
(2, 'auth', '0001_initial', '2026-05-07 07:33:50.558925'),
(3, 'admin', '0001_initial', '2026-05-07 07:33:50.626237'),
(4, 'admin', '0002_logentry_remove_auto_add', '2026-05-07 07:33:50.633315'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2026-05-07 07:33:50.640313'),
(6, 'contenttypes', '0002_remove_content_type_name', '2026-05-07 07:33:50.681541'),
(7, 'auth', '0002_alter_permission_name_max_length', '2026-05-07 07:33:50.711487'),
(8, 'auth', '0003_alter_user_email_max_length', '2026-05-07 07:33:50.723587'),
(9, 'auth', '0004_alter_user_username_opts', '2026-05-07 07:33:50.728593'),
(10, 'auth', '0005_alter_user_last_login_null', '2026-05-07 07:33:50.752565'),
(11, 'auth', '0006_require_contenttypes_0002', '2026-05-07 07:33:50.755572'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2026-05-07 07:33:50.762073'),
(13, 'auth', '0008_alter_user_username_max_length', '2026-05-07 07:33:50.774293'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2026-05-07 07:33:50.785668'),
(15, 'auth', '0010_alter_group_name_max_length', '2026-05-07 07:33:50.796943'),
(16, 'auth', '0011_update_proxy_permissions', '2026-05-07 07:33:50.803938'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2026-05-07 07:33:50.816993'),
(18, 'sessions', '0001_initial', '2026-05-07 07:33:50.834989'),
(19, 'sop', '0001_initial', '2026-05-07 07:33:51.501918'),
(20, 'sop', '0002_client_userclientmap', '2026-05-07 07:33:51.585489'),
(21, 'sop', '0003_remove_userclientmap_client_delete_client_and_more', '2026-05-07 07:33:52.107290'),
(22, 'sop', '0004_mediabucket_created_by', '2026-05-07 07:33:52.152191'),
(23, 'sop', '0005_alter_mediafile_file', '2026-05-07 07:33:52.158181'),
(24, 'sop', '0006_clientusermap', '2026-05-07 07:33:52.169401'),
(25, 'sop', '0007_delete_clientusermap', '2026-05-07 07:33:52.177372'),
(26, 'sop', '0008_clientusermap', '2026-05-07 07:33:52.195843'),
(27, 'sop', '0009_userprofile', '2026-05-07 07:33:52.246889'),
(28, 'sop', '0010_delete_userprofile', '2026-05-07 07:33:52.256887'),
(29, 'sop', '0011_machineruntime', '2026-05-07 07:33:52.268728'),
(30, 'sop', '0012_client', '2026-05-07 07:33:52.282732'),
(31, 'sop', '0013_alter_client_database_name', '2026-05-07 07:33:52.363341');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_admin`
--

CREATE TABLE `sop_admin` (
  `id` bigint(20) NOT NULL,
  `admin_username` varchar(150) DEFAULT NULL,
  `admin_password` varchar(150) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_client`
--

CREATE TABLE `sop_client` (
  `id` bigint(20) NOT NULL,
  `username` varchar(150) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `database_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_clientusermap`
--

CREATE TABLE `sop_clientusermap` (
  `id` bigint(20) NOT NULL,
  `username` varchar(150) NOT NULL,
  `db_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_displaytv`
--

CREATE TABLE `sop_displaytv` (
  `id` bigint(20) NOT NULL,
  `display_number` varchar(100) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_machineruntime`
--

CREATE TABLE `sop_machineruntime` (
  `id` bigint(20) NOT NULL,
  `url` varchar(500) NOT NULL,
  `created_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_mediabucket`
--

CREATE TABLE `sop_mediabucket` (
  `id` bigint(20) NOT NULL,
  `file` varchar(100) NOT NULL,
  `folder_name` varchar(100) DEFAULT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `sequence` int(10) UNSIGNED NOT NULL CHECK (`sequence` >= 0),
  `created_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_mediacontent`
--

CREATE TABLE `sop_mediacontent` (
  `id` bigint(20) NOT NULL,
  `duration` int(11) NOT NULL,
  `filename` varchar(100) DEFAULT NULL,
  `is_published` tinyint(1) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `display_tv_id` bigint(20) NOT NULL,
  `production_line_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_mediafile`
--

CREATE TABLE `sop_mediafile` (
  `id` bigint(20) NOT NULL,
  `file` varchar(100) NOT NULL,
  `order` varchar(50) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `media_content_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_mediasystem`
--

CREATE TABLE `sop_mediasystem` (
  `id` bigint(20) NOT NULL,
  `duration` int(11) NOT NULL,
  `is_published` tinyint(1) NOT NULL,
  `production_line_id` bigint(20) DEFAULT NULL,
  `select_folder_id` bigint(20) NOT NULL,
  `select_tv_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_productionadmin`
--

CREATE TABLE `sop_productionadmin` (
  `id` bigint(20) NOT NULL,
  `admin_username` varchar(150) DEFAULT NULL,
  `admin_password` varchar(150) DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_productionline`
--

CREATE TABLE `sop_productionline` (
  `id` bigint(20) NOT NULL,
  `productionline_name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `active_line` tinyint(1) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `tv_order` longtext DEFAULT NULL,
  `created_by_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_productionlinetv`
--

CREATE TABLE `sop_productionlinetv` (
  `id` bigint(20) NOT NULL,
  `status` varchar(100) NOT NULL,
  `display_tv_id` bigint(20) NOT NULL,
  `production_line_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_productionline_display_tv`
--

CREATE TABLE `sop_productionline_display_tv` (
  `id` bigint(20) NOT NULL,
  `productionline_id` bigint(20) NOT NULL,
  `displaytv_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_statustv`
--

CREATE TABLE `sop_statustv` (
  `id` bigint(20) NOT NULL,
  `status` varchar(100) NOT NULL,
  `time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `tvid_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_storagetv`
--

CREATE TABLE `sop_storagetv` (
  `id` bigint(20) NOT NULL,
  `storage` varchar(100) NOT NULL,
  `time` datetime(6) NOT NULL,
  `updated_time` datetime(6) NOT NULL,
  `tvid_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sop_volumetv`
--

CREATE TABLE `sop_volumetv` (
  `id` bigint(20) NOT NULL,
  `volume_tv` int(11) NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  `displaytv_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `sop_admin`
--
ALTER TABLE `sop_admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `sop_admin_created_by_id_132278dd_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `sop_client`
--
ALTER TABLE `sop_client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `sop_clientusermap`
--
ALTER TABLE `sop_clientusermap`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sop_clientusermap_username_db_name_5c08d9d6_uniq` (`username`,`db_name`);

--
-- Indexes for table `sop_displaytv`
--
ALTER TABLE `sop_displaytv`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_displaytv_user_id_7b695bce_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `sop_machineruntime`
--
ALTER TABLE `sop_machineruntime`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sop_mediabucket`
--
ALTER TABLE `sop_mediabucket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_mediabucket_created_by_id_9aa42c3a_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `sop_mediacontent`
--
ALTER TABLE `sop_mediacontent`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_mediacontent_production_line_id_59757c19_fk_sop_produ` (`production_line_id`),
  ADD KEY `sop_mediacontent_display_tv_id_ac6778bc_fk_sop_displaytv_id` (`display_tv_id`);

--
-- Indexes for table `sop_mediafile`
--
ALTER TABLE `sop_mediafile`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_mediafile_media_content_id_f95c3ac4_fk_sop_mediacontent_id` (`media_content_id`);

--
-- Indexes for table `sop_mediasystem`
--
ALTER TABLE `sop_mediasystem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_mediasystem_production_line_id_9a2cd5f0_fk_sop_produ` (`production_line_id`),
  ADD KEY `sop_mediasystem_select_folder_id_220d8a93_fk_sop_mediabucket_id` (`select_folder_id`),
  ADD KEY `sop_mediasystem_select_tv_id_b24ff537_fk_sop_displaytv_id` (`select_tv_id`);

--
-- Indexes for table `sop_productionadmin`
--
ALTER TABLE `sop_productionadmin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `sop_productionadmin_created_by_id_4cb46dfe_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `sop_productionline`
--
ALTER TABLE `sop_productionline`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_productionline_created_by_id_2e59dc37_fk_auth_user_id` (`created_by_id`);

--
-- Indexes for table `sop_productionlinetv`
--
ALTER TABLE `sop_productionlinetv`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_productionlinetv_display_tv_id_41b4935b_fk_sop_displaytv_id` (`display_tv_id`),
  ADD KEY `sop_productionlinetv_production_line_id_aff556cd_fk_sop_produ` (`production_line_id`);

--
-- Indexes for table `sop_productionline_display_tv`
--
ALTER TABLE `sop_productionline_display_tv`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sop_productionline_displ_productionline_id_displa_503fb590_uniq` (`productionline_id`,`displaytv_id`),
  ADD KEY `sop_productionline_d_displaytv_id_81edbeae_fk_sop_displ` (`displaytv_id`);

--
-- Indexes for table `sop_statustv`
--
ALTER TABLE `sop_statustv`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_statustv_tvid_id_39a598f3_fk_sop_displaytv_id` (`tvid_id`);

--
-- Indexes for table `sop_storagetv`
--
ALTER TABLE `sop_storagetv`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sop_storagetv_tvid_id_21c922e8_fk_sop_displaytv_id` (`tvid_id`);

--
-- Indexes for table `sop_volumetv`
--
ALTER TABLE `sop_volumetv`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `displaytv_id` (`displaytv_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `sop_admin`
--
ALTER TABLE `sop_admin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_client`
--
ALTER TABLE `sop_client`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_clientusermap`
--
ALTER TABLE `sop_clientusermap`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_displaytv`
--
ALTER TABLE `sop_displaytv`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_machineruntime`
--
ALTER TABLE `sop_machineruntime`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_mediabucket`
--
ALTER TABLE `sop_mediabucket`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_mediacontent`
--
ALTER TABLE `sop_mediacontent`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_mediafile`
--
ALTER TABLE `sop_mediafile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_mediasystem`
--
ALTER TABLE `sop_mediasystem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_productionadmin`
--
ALTER TABLE `sop_productionadmin`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_productionline`
--
ALTER TABLE `sop_productionline`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_productionlinetv`
--
ALTER TABLE `sop_productionlinetv`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_productionline_display_tv`
--
ALTER TABLE `sop_productionline_display_tv`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_statustv`
--
ALTER TABLE `sop_statustv`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_storagetv`
--
ALTER TABLE `sop_storagetv`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `sop_volumetv`
--
ALTER TABLE `sop_volumetv`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sop_admin`
--
ALTER TABLE `sop_admin`
  ADD CONSTRAINT `sop_admin_created_by_id_132278dd_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `sop_admin_user_id_9daae270_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sop_displaytv`
--
ALTER TABLE `sop_displaytv`
  ADD CONSTRAINT `sop_displaytv_user_id_7b695bce_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sop_mediabucket`
--
ALTER TABLE `sop_mediabucket`
  ADD CONSTRAINT `sop_mediabucket_created_by_id_9aa42c3a_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sop_mediacontent`
--
ALTER TABLE `sop_mediacontent`
  ADD CONSTRAINT `sop_mediacontent_display_tv_id_ac6778bc_fk_sop_displaytv_id` FOREIGN KEY (`display_tv_id`) REFERENCES `sop_displaytv` (`id`),
  ADD CONSTRAINT `sop_mediacontent_production_line_id_59757c19_fk_sop_produ` FOREIGN KEY (`production_line_id`) REFERENCES `sop_productionline` (`id`);

--
-- Constraints for table `sop_mediafile`
--
ALTER TABLE `sop_mediafile`
  ADD CONSTRAINT `sop_mediafile_media_content_id_f95c3ac4_fk_sop_mediacontent_id` FOREIGN KEY (`media_content_id`) REFERENCES `sop_mediacontent` (`id`);

--
-- Constraints for table `sop_mediasystem`
--
ALTER TABLE `sop_mediasystem`
  ADD CONSTRAINT `sop_mediasystem_production_line_id_9a2cd5f0_fk_sop_produ` FOREIGN KEY (`production_line_id`) REFERENCES `sop_productionline` (`id`),
  ADD CONSTRAINT `sop_mediasystem_select_folder_id_220d8a93_fk_sop_mediabucket_id` FOREIGN KEY (`select_folder_id`) REFERENCES `sop_mediabucket` (`id`),
  ADD CONSTRAINT `sop_mediasystem_select_tv_id_b24ff537_fk_sop_displaytv_id` FOREIGN KEY (`select_tv_id`) REFERENCES `sop_displaytv` (`id`);

--
-- Constraints for table `sop_productionadmin`
--
ALTER TABLE `sop_productionadmin`
  ADD CONSTRAINT `sop_productionadmin_created_by_id_4cb46dfe_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `sop_productionadmin_user_id_0a4e37b2_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sop_productionline`
--
ALTER TABLE `sop_productionline`
  ADD CONSTRAINT `sop_productionline_created_by_id_2e59dc37_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `sop_productionlinetv`
--
ALTER TABLE `sop_productionlinetv`
  ADD CONSTRAINT `sop_productionlinetv_display_tv_id_41b4935b_fk_sop_displaytv_id` FOREIGN KEY (`display_tv_id`) REFERENCES `sop_displaytv` (`id`),
  ADD CONSTRAINT `sop_productionlinetv_production_line_id_aff556cd_fk_sop_produ` FOREIGN KEY (`production_line_id`) REFERENCES `sop_productionline` (`id`);

--
-- Constraints for table `sop_productionline_display_tv`
--
ALTER TABLE `sop_productionline_display_tv`
  ADD CONSTRAINT `sop_productionline_d_displaytv_id_81edbeae_fk_sop_displ` FOREIGN KEY (`displaytv_id`) REFERENCES `sop_displaytv` (`id`),
  ADD CONSTRAINT `sop_productionline_d_productionline_id_1de3e8d5_fk_sop_produ` FOREIGN KEY (`productionline_id`) REFERENCES `sop_productionline` (`id`);

--
-- Constraints for table `sop_statustv`
--
ALTER TABLE `sop_statustv`
  ADD CONSTRAINT `sop_statustv_tvid_id_39a598f3_fk_sop_displaytv_id` FOREIGN KEY (`tvid_id`) REFERENCES `sop_displaytv` (`id`);

--
-- Constraints for table `sop_storagetv`
--
ALTER TABLE `sop_storagetv`
  ADD CONSTRAINT `sop_storagetv_tvid_id_21c922e8_fk_sop_displaytv_id` FOREIGN KEY (`tvid_id`) REFERENCES `sop_displaytv` (`id`);

--
-- Constraints for table `sop_volumetv`
--
ALTER TABLE `sop_volumetv`
  ADD CONSTRAINT `sop_volumetv_displaytv_id_98fcb850_fk_sop_displaytv_id` FOREIGN KEY (`displaytv_id`) REFERENCES `sop_displaytv` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
