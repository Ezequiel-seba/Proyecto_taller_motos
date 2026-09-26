-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-09-2026 a las 02:25:49
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pp2_taller_motos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `idclientes` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`idclientes`, `nombre`, `apellido`, `telefono`, `direccion`) VALUES
(1, 'juan', 'ramirez', '3704112233', 'malvinas 123'),
(3, 'daniela', 'Mesa', '3704111222', '25 de mayo'),
(4, 'miguel', 'ramirez', '3704112233', '20 de junio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mecanicos`
--

CREATE TABLE `mecanicos` (
  `idmecanicos` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `documento` varchar(20) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `mecanicos`
--

INSERT INTO `mecanicos` (`idmecanicos`, `nombre`, `apellido`, `documento`, `telefono`, `direccion`) VALUES
(1, 'marcelo', 'Jahn', '39450654', '3704998877', 'fontana 321');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `motos`
--

CREATE TABLE `motos` (
  `idmotos` int(11) NOT NULL,
  `idclientes` int(11) NOT NULL,
  `marca` varchar(50) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `patente` varchar(15) NOT NULL,
  `ano` int(11) NOT NULL,
  `foto` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `motos`
--

INSERT INTO `motos` (`idmotos`, `idclientes`, `marca`, `modelo`, `patente`, `ano`, `foto`) VALUES
(1, 1, 'honda', 'Wave 110S', 'asc55500', 2020, NULL),
(2, 3, 'motomel', 'B110', 'zxc121233', 2015, NULL),
(3, 4, 'honda', 'Wave 110S', 'sdf345', 2010, NULL),
(4, 4, 'honda', 'Wave 110S', 'dfg567', 2020, 'dfg567_Honda_wave.jpg'),
(5, 1, 'motomel', 'Wave 110S', '223332', 0, NULL),
(6, 3, 'honda', 'B110', '21111111111111', 0, NULL),
(7, 4, 'honda', 'Wave 110S', '21212212dsa', 0, NULL),
(8, 1, 'motomel', 'B110', 'sadasds', 2012, NULL),
(9, 1, 'honda', 'Wave 110S', 'fty567', 0, NULL),
(10, 3, 'motomel', 'Wave 110S', '987dfs', 0, NULL),
(11, 4, 'motomel', 'B110', '123456', 2023, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `idservicios` int(11) NOT NULL,
  `idmotos` int(11) NOT NULL,
  `Descripcion` text NOT NULL,
  `fecha_ingreso` date NOT NULL,
  `fecha_salida` date DEFAULT NULL,
  `costo` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','en_proceso','finalizado') NOT NULL DEFAULT 'pendiente',
  `idmecanicos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`idservicios`, `idmotos`, `Descripcion`, `fecha_ingreso`, `fecha_salida`, `costo`, `estado`, `idmecanicos`) VALUES
(1, 1, 'emparchado de goma', '2025-05-12', NULL, 20000.00, 'pendiente', 1),
(2, 2, 'servi completo', '2025-06-25', NULL, 50000.00, 'en_proceso', 1),
(3, 3, 'reparacion de cadena', '2019-05-19', NULL, 40000.00, 'pendiente', 1),
(4, 2, 'revision para detectar problema', '2022-07-20', NULL, 100000.00, 'finalizado', 1),
(6, 1, 'revicion completa', '2020-11-23', NULL, 10000.00, 'en_proceso', 1),
(7, 4, 'problema de cadena', '2020-02-12', NULL, 20000.00, 'pendiente', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `idusuarios` int(11) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`idusuarios`, `correo`, `contrasena`) VALUES
(1, 'admin', '$2b$12$T4LFNCx7oYBCNSTxGTevu.NsEG3BuZGqxvJJQEtEu27xwfsrLcl7K'),
(2, 'sebastian@gmail.com', '$2b$12$lHgIusn1d0Eqj3KgicWdueorD586BqWAe1BgKxxlRvcqXJsjsSs/W'),
(3, 'rene@gmail.com', '$2b$12$TtufNnFs292ua5ECm6NCgeXJdmqktGouP1TLclMsTCdCtblGvnG5O');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idclientes`);

--
-- Indices de la tabla `mecanicos`
--
ALTER TABLE `mecanicos`
  ADD PRIMARY KEY (`idmecanicos`),
  ADD UNIQUE KEY `documento` (`documento`);

--
-- Indices de la tabla `motos`
--
ALTER TABLE `motos`
  ADD PRIMARY KEY (`idmotos`),
  ADD UNIQUE KEY `patente` (`patente`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`idservicios`),
  ADD KEY `idmecanicos` (`idmecanicos`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`idusuarios`),
  ADD UNIQUE KEY `usuario` (`correo`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `idclientes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `mecanicos`
--
ALTER TABLE `mecanicos`
  MODIFY `idmecanicos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `motos`
--
ALTER TABLE `motos`
  MODIFY `idmotos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `idservicios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `idusuarios` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD CONSTRAINT `servicios_ibfk_1` FOREIGN KEY (`idmecanicos`) REFERENCES `mecanicos` (`idmecanicos`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
