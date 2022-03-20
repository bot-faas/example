<?php

use App\Handler;

require_once 'vendor/autoload.php';


if ($_SERVER['REQUEST_METHOD'] === 'POST' && $_SERVER['REQUEST_URI'] === '/handle') {
    $data = file_get_contents('php://input');
    if (!$data) {
        return;
    }
    $data = json_decode($data);
    $data = json_decode($data->data);
    $handler = new Handler();
    $method = new ReflectionMethod($handler, 'handle');
    $params = $method->getParameters();
    $className = $params[0]->getClass();
    $arg = new $className->name;
    foreach ($data as $k => $v) {
        if (property_exists($arg, $k)) {
            $arg->$k = $v;
        }
    }
    echo json_encode($handler->handle($arg), JSON_UNESCAPED_UNICODE);
}
