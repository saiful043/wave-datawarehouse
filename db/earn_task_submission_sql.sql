-- -------------------------------------------------------------
-- TablePlus 27.1.0(830)
--
-- https://tableplus.com/
--
-- Database: wave_datawarehouse
-- Generation Time: 2026-10-28 14:21:44.7010
-- -------------------------------------------------------------


DROP TABLE IF EXISTS "public"."earn_task_submission";
-- Table Definition
CREATE TABLE "public"."earn_task_submission" (
    "id" int8 NOT NULL,
    "status" varchar(20) NOT NULL,
    "comments" text,
    "submitted_at" timestamptz NOT NULL,
    "district_id" int4 NOT NULL,
    "division_id" int4 NOT NULL,
    "upazila_id" int4 NOT NULL,
    "user_id" int4,
    "task_template_id" int8 NOT NULL,
    "percentage_completion" numeric(5,2) NOT NULL,
    PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS "public"."earn_parent_task";
-- Table Definition
CREATE TABLE "public"."earn_parent_task" (
    "id" int8 NOT NULL,
    "task_id" varchar(100) NOT NULL,
    "name" varchar(255) NOT NULL,
    "created_at" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS "public"."earn_task_template";
-- Table Definition
CREATE TABLE "public"."earn_task_template" (
    "id" int8 NOT NULL,
    "task_name" varchar(400) NOT NULL,
    "created_at" timestamptz NOT NULL,
    "updated_at" timestamptz NOT NULL,
    "level" varchar(50) NOT NULL,
    "earn_parent_task_id" int8,
    "planned_period_from" date,
    "planned_period_to" date,
    "task_code" varchar(100),
    PRIMARY KEY ("id")
);

INSERT INTO "public"."earn_task_submission" ("id", "status", "comments", "submitted_at", "district_id", "division_id", "upazila_id", "user_id", "task_template_id", "percentage_completion") VALUES
(1, 'In Progress', 'আমি সব কাজ শেষ করেছি', '2026-10-28 10:18:53.131094+06', 36, 9, 387, 3, 1, 12.00),
(2, 'Not Started', '', '2026-10-10 18:48:54.275789+06', 64, 3, 586, 4, 1, 0.00),
(3, 'In Progress', 'ghg', '2026-10-26 16:07:28.36034+06', 36, 9, 387, 3, 9, 10.00),
(4, 'Delayed', '', '2026-10-27 14:36:46.171632+06', 36, 9, 387, 3, 8, 0.00),
(5, 'Not Started', '', '2026-10-10 22:58:18.469812+06', 36, 9, 387, 3, 7, 0.00),
(6, 'Not Started', 'tefgcbvn', '2026-10-26 16:05:54.383904+06', 64, 3, 580, 2, 9, 0.00),
(7, 'Completed', 'gfhhgjgj test', '2026-10-26 16:08:03.504305+06', 64, 3, 586, 4, 9, 100.00),
(8, 'Not Started', '', '2026-10-27 12:12:58.435822+06', 64, 3, 586, 4, 8, 0.00),
(9, 'Not Started', '', '2026-10-27 12:13:09.985692+06', 64, 3, 586, 4, 7, 0.00),
(10, 'In Progress', '', '2026-10-28 10:27:37.468945+06', 36, 9, 387, 3, 2, 3.00);

INSERT INTO "public"."earn_parent_task" ("id", "task_id", "name", "created_at", "updated_at") VALUES
(1, 'D1', 'Project Mobilization and Inception Report', '2026-10-26 12:52:01.469992+06', '2026-10-26 12:52:01.469992+06'),
(2, 'D2', 'Beneficiary Identification and Selection', '2026-10-26 12:53:59.547014+06', '2026-10-26 12:53:59.547014+06'),
(3, 'D3', 'Community Groups Formation and Trained at Union Level', '2026-10-26 12:53:59.547014+06', '2026-10-26 12:53:59.547014+06'),
(4, 'D4', 'Site Selection and Establishment of VLTCs for SEB and EDT Only', '2026-10-26 12:56:22.170969+06', '2026-10-26 12:56:22.170969+06'),
(5, 'D5', 'Number of Community Group (CG) Meetings', '2026-10-26 12:56:22.170969+06', '2026-10-26 12:56:22.170969+06'),
(6, 'D6', 'Upazila-Level Plan Approved', '2026-10-26 12:56:22.170969+06', '2026-10-26 12:56:22.170969+06'),
(7, 'D7', 'Number of SEB and EDT Only training completed beneficiaries', '2026-10-26 12:56:22.170969+06', '2026-10-26 12:56:22.170969+06'),
(8, 'D8', 'Identification of Trades', '2026-10-26 12:56:22.170969+06', '2026-10-26 12:56:22.170969+06'),
(9, 'D9', 'Number of VLTCs Established for Skill Training', '2026-10-26 12:56:22.170969+06', '2026-10-26 12:56:22.170969+06'),
(10, 'D10', 'Distribution of Beneficiaries by Skills, Trades and Categories', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(11, 'D11', 'Number of Enrolled Beneficiaries for Skills Training', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(12, 'D12', 'Number of total beneficiaries completed Skills+SEB & EDT', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(13, 'D13', 'Number of Beneficiaries Completed Skills Training', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(14, 'D14', 'Leadership, Life Skills and Climate Action Training', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(15, 'D15', 'Number of Beneficiaries Employed/Self-Employed (with or without Seed Financing)', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(16, 'D16', 'Number of Beneficiaries Started Internship', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06'),
(17, 'D17', 'Share of Identified Beneficiaries Employed/Self-Employed/Returned to Employment', '2026-10-26 12:58:58.819393+06', '2026-10-26 12:58:58.819393+06');

INSERT INTO "public"."earn_task_template" ("id", "task_name", "created_at", "updated_at", "level", "earn_parent_task_id", "planned_period_from", "planned_period_to", "task_code") VALUES
(1, 'Preparation and submission of the Inception Report', '2026-10-10 18:38:17.5119+06', '2026-10-27 14:41:12.80655+06', 'HQ', 1, '2026-07-01', '2026-07-31', 'A.1.9'),
(2, 'Development of Risk Management Plan', '2026-10-10 21:19:50.426815+06', '2026-10-27 14:40:21.513299+06', 'HQ', 1, '2026-07-01', '2026-08-31', 'A.1.8'),
(3, 'Development of Monitoring Framework and Quality Assurance Plan', '2026-10-10 21:20:30.272582+06', '2026-10-27 14:39:42.753537+06', 'HQ', 1, '2026-08-01', '2026-09-30', 'A.1.7'),
(4, 'Preparation and submission of Annual Work Plan (AWP) and Implementation calendar', '2026-10-10 21:21:09.970745+06', '2026-10-27 14:38:36.23614+06', 'HQ', 1, '2026-07-01', '2026-08-31', 'A.1.6'),
(5, 'Establishment of MEL, MIS, Data Management System, safeguarding and reporting systems', '2026-10-10 21:21:42.026313+06', '2026-10-27 14:37:55.214696+06', 'HQ', 1, '2026-07-01', '2026-10-31', 'A.1.5'),
(6, 'Procurement of logistics and equipment and establishment of office', '2026-10-10 21:22:27.665271+06', '2026-10-27 14:30:57.189322+06', 'HQ', 1, '2026-07-01', '2026-09-30', 'A.1.4'),
(7, 'Deployment of project staff', '2026-10-10 21:22:56.640391+06', '2026-10-26 15:29:58.620584+06', 'HQ', 1, '2026-07-01', '2026-08-31', 'A.1.3'),
(8, 'Kick-off meetings with PMU and SPs', '2026-10-10 21:23:59.981395+06', '2026-10-26 15:29:21.545274+06', 'HQ', 1, '2026-07-01', '2026-07-31', 'A.1.2'),
(9, 'Contract signing and project commencement', '2026-10-10 21:24:37.48319+06', '2026-10-26 15:28:14.282163+06', 'HQ', 1, '2026-07-01', '2026-07-31', 'A-1.1'),
(10, 'Obtain PMU approval', '2026-10-27 14:41:52.136798+06', '2026-10-27 14:41:52.136812+06', 'HQ', 1, '2026-08-01', '2026-08-31', 'A.1.10'),
(11, 'Finalize beneficiary selection criteria and design survey tools.', '2026-10-27 14:46:42.484605+06', '2026-10-27 14:46:42.484626+06', 'Upazila', 2, '2026-08-01', '2026-09-30', 'A.2.1'),
(12, 'Finalize beneficiary selection criteria and design survey tools.', '2026-10-27 14:59:32.769116+06', '2026-10-27 14:59:32.769159+06', 'Upazila', 2, '2026-08-01', '2026-09-30', 'A.2.1'),
(13, 'Assign project staff for beneficiary identification', '2026-10-27 15:07:18.971524+06', '2026-10-27 15:07:18.971537+06', 'Upazila', 2, '2026-09-01', '2026-11-30', 'A.2.2'),
(14, 'Conduct community awareness campaign', '2026-10-27 15:08:07.880387+06', '2026-10-27 15:08:07.880398+06', 'Upazila', 2, '2026-09-01', '2027-12-31', 'A.2.3'),
(15, 'Confirm identifying NEET youth, verifying eligibility criteria, collecting socio-economic data, disability, screening, gender vulnerability assessment, livelihood profiling, education profiling, during beneficiary identification', '2026-10-27 15:09:28.919503+06', '2026-10-27 15:09:28.919518+06', 'Upazila', 2, '2026-09-01', '2027-12-31', 'A.2.4'),
(16, 'Insert data into the MIS cell portal as part of data generation and beneficiary identification process', '2026-10-27 15:10:17.232483+06', '2026-10-27 15:10:17.232492+06', 'Upazila', 2, '2026-09-01', '2027-12-31', 'A.2.5'),
(17, 'Validate, clean, and compile beneficiary list', '2026-10-27 15:11:00.213042+06', '2026-10-27 15:11:00.213052+06', 'Upazila', 2, '2026-11-01', '2027-12-31', 'A.2.6'),
(18, 'Submit beneficiary list', '2026-10-27 15:11:52.506395+06', '2026-10-27 15:11:52.506406+06', 'Upazila', 2, '2026-12-01', '2027-12-31', 'A.2.7'),
(19, 'Form Community Groups (CGs) at the union level perform community mapping, identifying local leaders and selecting CG members to support community engagement and project implementation.', '2026-10-27 15:22:52.304513+06', '2026-10-27 15:22:52.304551+06', 'Upazila', 3, '2026-08-01', '2026-09-30', 'A.3.1'),
(20, 'Detailed CG data entered in the MIS portal', '2026-10-27 15:23:38.490954+06', '2026-10-27 15:23:38.490974+06', 'Upazila', 3, '2026-08-01', '2027-08-31', 'A.3.2'),
(21, 'Conduct CG meeting at union level', '2026-10-27 15:24:29.75151+06', '2026-10-27 15:28:38.101226+06', 'Upazila', 3, '2026-09-01', '2028-12-31', 'A.3.3'),
(22, 'Conduct a 3-day foundation and capacity building training for CG members to build core awareness and advocacy skills on climate change impacts, social norms, SEA/SH, and environmental issues.', '2026-10-27 15:25:05.296416+06', '2026-10-27 15:25:05.296428+06', 'Upazila', 3, '2026-09-01', '2027-09-30', 'A.3.4'),
(23, 'Organize 1-day bi-annual refresher training to reinforce and update CG capacities.', '2026-10-27 15:26:03.464728+06', '2026-10-27 15:26:03.46474+06', 'Upazila', 3, '2027-02-01', '2028-04-30', 'A.3.5'),
(24, 'Identify appropriate village-level training center sites for SEB & EDT in consultation with CGs, ensuring accessibility, safety, and women-friendly environments', '2026-10-27 15:33:11.401925+06', '2026-10-27 15:33:45.360001+06', 'Upazila', 4, '2026-08-01', '2027-08-31', 'A.4.1'),
(25, 'Select suitable VLTC location and infrastructure to include PWD, third gender/hijra individuals in the training program.', '2026-10-27 15:34:33.256461+06', '2026-10-27 15:36:00.857537+06', 'Upazila', 4, '2026-08-01', '2027-08-31', 'A.4.2'),
(26, 'Prepare a detailed year-wise SEB & EDT training implementation plan in selected VLTCs, specifying number of beneficiaries, trades, and locations', '2026-10-27 15:36:57.051179+06', '2026-10-27 15:36:57.051189+06', 'Upazila', 4, '2026-08-01', '2028-08-31', 'A.4.3'),
(27, 'Obtain formal approval of the year-wise VLTC plan from the PMU', '2026-10-27 15:38:19.932277+06', '2026-10-27 15:38:19.932287+06', 'Upazila', 4, '2026-09-01', '2028-08-31', 'A.4.4'),
(28, 'Establish Village Level Training Centers (VLTCs). Set up the training center with all facilities (furniture, fixture, training equipment, fan, provision of pure drinking water, separate toilets for male and women trainees and Occupational Health and Safety (OHS) equipment, CCTV, electronic attendance, monitoring system, high speed internet).', '2026-10-27 15:42:08.650018+06', '2026-10-27 15:42:08.65003+06', 'Upazila', 4, '2026-10-01', '2028-01-31', 'A.4.5'),
(29, 'Ensure all VLTCs are built or renovated using climate-friendly practices, materials, and technologies including adequate privacy, security, childcare support, etc.', '2026-10-27 15:43:04.60812+06', '2026-10-27 15:44:20.348264+06', 'Upazila', 4, '2026-11-01', '2027-12-31', 'A.4.6'),
(30, 'Equip VLTC with fire safety equipment, conduct regular safety drills, and implement incident reporting protocols to ensure the health and safety of trainees & staff', '2026-10-27 15:45:00.835928+06', '2026-10-27 15:45:00.835937+06', 'Upazila', 4, '2026-11-01', '2027-12-31', 'A.4.7'),
(31, 'Record and upload detailed facility-level information for each VLTC into the MIS portal to support tracking and project oversight', '2026-10-27 15:45:39.976692+06', '2026-10-27 15:45:39.976703+06', 'Upazila', 4, '2026-12-01', '2027-12-31', 'A.4.8'),
(32, 'Print/produce communication materials (Leaflet, banner, poster, miking, SMS, festoon, signboard, circle branding, billboard)', '2026-10-27 15:46:29.502663+06', '2026-10-27 15:46:29.502675+06', 'Upazila', 4, '2026-10-01', '2027-06-30', 'A.4.9'),
(33, 'Ensure the availability of a functional laptop with the required configuration (to be finalized with LGED MIS cell) and a high-speed internet connection at each VLTC office for smooth data entry and communication', '2026-10-27 15:47:03.069951+06', '2026-10-27 15:47:03.06996+06', 'Upazila', 4, '2026-11-01', '2027-12-31', 'A.4.10'),
(34, 'Insert all relevant data on VLTCs into the MIS portal for centralized monitoring and reporting', '2026-10-27 15:47:40.978601+06', '2026-10-27 15:47:40.978615+06', 'Upazila', 4, '2026-11-01', '2027-12-31', 'A.4.11'),
(35, 'Prepare meeting calendar and organize monthly CGs meeting and SPs will prepare the monthly meeting minutes.', '2026-10-27 15:48:23.818957+06', '2026-10-27 15:48:23.818972+06', 'Upazila', 5, '2026-08-01', '2026-09-30', 'A.5.1'),
(36, 'Conduct monthly Uthan Boithaks (Courtyard Meetings) in each union during the VLTCs operation with the support of CGs, record attendance and prepare the upazila wise consolidated monthly event report', '2026-10-27 15:49:20.636393+06', '2026-10-27 15:49:20.636405+06', 'Upazila', 5, '2026-10-01', '2028-06-30', 'A.5.2'),
(37, 'Establish Upazila Coordination Committees (UCCs) to oversee coordination and collaboration at the sub-district level.', '2026-10-27 15:50:16.048429+06', '2026-10-27 15:50:16.048444+06', 'Upazila', 6, '2026-09-01', '2027-10-31', 'A.6.1'),
(38, 'Prepare quarter/year-wise plan for VLTCs by union and villages (Number of beneficiaries, trades, locations etc.)', '2026-10-27 15:51:03.998126+06', '2026-10-27 15:51:03.998135+06', 'Upazila', 6, '2026-09-01', '2027-10-31', 'A.6.2'),
(39, 'Mapping of school, college, madrasas and youth clubs', '2026-10-27 15:51:37.481218+06', '2026-10-27 15:51:37.48123+06', 'Upazila', 6, '2026-09-01', '2027-10-31', 'A.6.3'),
(40, 'Assist in establishing and building capacity of Union Youth Information Centers (UYICs).', '2026-10-27 15:52:11.032658+06', '2026-10-27 15:52:11.032667+06', 'Upazila', 6, '2026-09-01', '2027-10-31', 'A.6.4'),
(41, 'Adopt the PMU-approved communication strategy to raise awareness and engage local stakeholders effectively', '2026-10-27 15:52:45.585814+06', '2026-10-27 15:52:45.585826+06', 'Upazila', 6, '2026-09-01', '2027-10-31', 'A.6.5'),
(42, 'coordinate enrolment, training and employment activities by UCC.', '2026-10-27 15:53:33.861587+06', '2026-10-27 15:53:33.861596+06', 'Upazila', 6, '2026-09-01', '2027-10-31', 'A.6.6'),
(43, 'Organize quarterly UCC meetings (20 participants)', '2026-10-27 15:54:10.897735+06', '2026-10-27 15:54:10.897745+06', 'Upazila', 6, '2026-09-01', '2028-03-31', 'A.6.7'),
(44, 'Customization/development of SEB and EDT training manuals', '2026-10-27 16:03:35.084438+06', '2026-10-27 16:03:35.084481+06', 'Upazila', 7, '2026-09-01', '2026-09-30', 'A.7.1'),
(45, 'Ensure the availability of all required training and learning materials, including handouts and job aids, at the training centers', '2026-10-27 16:04:18.717428+06', '2026-10-27 16:04:18.717439+06', 'Upazila', 7, '2026-09-01', '2026-10-31', 'A.7.2'),
(46, 'Recruit facilitators and provide 3-days orientation on SEB & EDT training.', '2026-10-27 16:04:45.420914+06', '2026-10-27 16:04:45.420923+06', 'Upazila', 7, '2026-10-01', '2026-10-31', 'A.7.3'),
(47, 'Provide one month (120 hours) of SEB and EDT training as part of the VLTC training', '2026-10-27 16:05:18.69944+06', '2026-10-27 16:05:18.69945+06', 'Upazila', 7, '2026-11-01', '2028-03-31', 'A.7.4'),
(48, 'Deliver life skills, employability, entrepreneurship, digital literacy, financial literacy, climate awareness, career planning and green skills training', '2026-10-27 16:05:59.537058+06', '2026-10-27 16:05:59.537068+06', 'Upazila', 7, '2026-11-01', '2028-03-31', 'A.7.5'),
(49, 'Enter training attendance and completion data of SEB and EDT sessions into the MIS cell portal for tracking and reporting', '2026-10-27 16:06:32.591009+06', '2026-10-27 17:06:15.748408+06', 'Upazila', 7, '2026-11-01', '2028-03-31', 'A.7.6'),
(50, 'Enter training attendance and completion data of SEB and EDT sessions into the MIS cell portal for tracking and reporting', '2026-10-27 16:07:37.797007+06', '2026-10-27 16:07:37.79704+06', 'Upazila', 7, '2026-11-01', '2028-03-31', 'A.7.6'),
(51, 'Conduct assessment and issue professional certificates for completion of SEB and EDT to the successful participants', '2026-10-27 16:08:11.217191+06', '2026-10-27 16:08:11.217202+06', 'Upazila', 7, '2026-11-01', '2028-03-31', 'A.7.7');



-- Indices
CREATE UNIQUE INDEX earn_task_submission_task_template_id_upazila_id_c532eb09_uniq ON public.earn_task_submission USING btree (task_template_id, upazila_id);
CREATE INDEX earn_task_submission_district_id_5073c9fe ON public.earn_task_submission USING btree (district_id);
CREATE INDEX earn_task_submission_division_id_d67c9b92 ON public.earn_task_submission USING btree (division_id);
CREATE INDEX earn_task_submission_task_template_id_c516b514 ON public.earn_task_submission USING btree (task_template_id);
CREATE INDEX earn_task_submission_upazila_id_d1637341 ON public.earn_task_submission USING btree (upazila_id);
CREATE INDEX earn_task_submission_user_id_e10c3884 ON public.earn_task_submission USING btree (user_id);
ALTER TABLE "public"."earn_task_submission" ADD FOREIGN KEY ("division_id") REFERENCES "public"."core_location"("location_id");
ALTER TABLE "public"."earn_task_submission" ADD FOREIGN KEY ("user_id") REFERENCES "public"."auth_user"("id");
ALTER TABLE "public"."earn_task_submission" ADD FOREIGN KEY ("upazila_id") REFERENCES "public"."core_location"("location_id");
ALTER TABLE "public"."earn_task_submission" ADD FOREIGN KEY ("task_template_id") REFERENCES "public"."earn_task_template"("id");
ALTER TABLE "public"."earn_task_submission" ADD FOREIGN KEY ("district_id") REFERENCES "public"."core_location"("location_id");


-- Indices
CREATE UNIQUE INDEX earn_parent_task_task_id_key ON public.earn_parent_task USING btree (task_id);
CREATE INDEX earn_parent_task_task_id_a58f02e2_like ON public.earn_parent_task USING btree (task_id varchar_pattern_ops);


-- Indices
CREATE INDEX earn_task_template_earn_parent_task_id_3c5d9188 ON public.earn_task_template USING btree (earn_parent_task_id);
ALTER TABLE "public"."earn_task_template" ADD FOREIGN KEY ("earn_parent_task_id") REFERENCES "public"."earn_parent_task"("id");
