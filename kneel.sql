CREATE TABLE `Metals`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `metal` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);
CREATE TABLE `Sizes`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `carets` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);
CREATE TABLE `Styles`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `style` NVARCHAR(160) NOT NULL,
    `price` NUMERIC(5,2) NOT NULL
);

CREATE TABLE `Orders`
(
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `timestamp` INTEGER NOT NULL,
    `metalId` INTEGER NOT NULL,
    `sizeId` INTEGER NOT NULL,
    `styleId` INTEGER NOT NULL,
    FOREIGN KEY(`metalId`) REFERENCES `Metals`(`id`),
    FOREIGN KEY(`sizeId`) REFERENCES `Sizes`(`id`),
    FOREIGN KEY(`styleId`) REFERENCES `Styles`(`id`)
);

INSERT INTO `Metals` (`metal`, `price`) VALUES
('Gold', 45.99),
('Silver', 22.50),
('Platinum', 75.25),
('Titanium', 18.75),
('Copper', 8.99);

INSERT INTO `Styles` (`style`, `price`) VALUES
('Classic', 30.00),
('Vintage', 35.50),
('Modern', 40.25),
('Art Deco', 37.75),
('Bohemian', 27.99);

INSERT INTO `Sizes` (`carets`, `price`) VALUES
('1.0', 55.00),
('1.5', 65.50),
('2.0', 75.25),
('2.5', 85.75),
('3.0', 95.99);

INSERT INTO `Orders` (`timestamp`, `metalId`, `sizeId`, `styleId`) VALUES
(1635608767, 1, 3, 2),
(1635613215, 2, 4, 4),
(1635617658, 3, 1, 3),
(1635622106, 4, 2, 5),
(1635626553, 5, 5, 1),
(1635631001, 1, 2, 4),
(1635635448, 2, 4, 5),
(1635639896, 3, 1, 2),
(1635644343, 4, 3, 1),
(1635648791, 5, 5, 3);