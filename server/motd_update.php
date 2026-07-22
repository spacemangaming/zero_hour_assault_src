<?php
// motd_update.php — place this at spacemangaming.vineyard.haus/zero/
// GET  → returns motd.txt contents
// POST → overwrites motd.txt with raw request body (protected by secret key)

define('SECRET_KEY', 'changeme_secret');   // set this, and the same in telegram_bot.py
define('MOTD_FILE',  __DIR__ . '/motd.txt');

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    header('Content-Type: text/plain; charset=utf-8');
    echo file_exists(MOTD_FILE) ? file_get_contents(MOTD_FILE) : '';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $key = $_SERVER['HTTP_X_SECRET_KEY'] ?? '';
    if ($key !== SECRET_KEY) {
        http_response_code(401);
        echo 'Unauthorized';
        exit;
    }
    $body = file_get_contents('php://input');
    if (strlen($body) > 4096) {
        http_response_code(400);
        echo 'MOTD too long (max 4096 chars)';
        exit;
    }
    file_put_contents(MOTD_FILE, $body);
    http_response_code(200);
    echo 'OK';
    exit;
}

http_response_code(405);
echo 'Method not allowed';
