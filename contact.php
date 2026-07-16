<?php
// Native PHP Contact Form Handler
// Strictly no 3rd-party SaaS as per architectural rules.

header('Content-Type: application/json');

// Only allow POST requests
if ($_SERVER["REQUEST_METHOD"] !== "POST") {
    http_response_code(405);
    echo json_encode(["status" => "error", "message" => "Method not allowed"]);
    exit;
}

// Sanitize inputs
$name = isset($_POST['name']) ? strip_tags(trim($_POST['name'])) : '';
$email = isset($_POST['email']) ? filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL) : '';
$phone = isset($_POST['phone']) ? strip_tags(trim($_POST['phone'])) : '';
$service = isset($_POST['service']) ? strip_tags(trim($_POST['service'])) : '';
$message = isset($_POST['message']) ? strip_tags(trim($_POST['message'])) : '';

// Validation
if (empty($name) || empty($message) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(["status" => "error", "message" => "Please complete all required fields correctly."]);
    exit;
}

// Prepare Email
$to = "ozunaprinting@gmail.com";
$subject = "New Quote Request from $name - Ozuna Printing";

$email_content = "You have received a new quote request from the website.\n\n";
$email_content .= "Name: $name\n";
$email_content .= "Email: $email\n";
$email_content .= "Phone: $phone\n";
$email_content .= "Service Requested: $service\n\n";
$email_content .= "Message:\n$message\n";

$headers = "From: webmaster@ozunaprinting.com\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// Send Email
if (mail($to, $subject, $email_content, $headers)) {
    // Send Auto-Responder to Client
    $auto_subject = "Thank you for contacting Ozuna Printing";
    $auto_content = "Hi $name,\n\nThank you for reaching out to Ozuna Printing! We have received your request for a custom quote regarding '$service'.\n\nOur team will review your project details and get back to you shortly.\n\nBest regards,\nThe Ozuna Printing Team\n438-393-9465";
    $auto_headers = "From: ozunaprinting@gmail.com\r\n";
    mail($email, $auto_subject, $auto_content, $auto_headers);

    echo json_encode(["status" => "success", "message" => "Your request has been sent successfully!"]);
} else {
    http_response_code(500);
    echo json_encode(["status" => "error", "message" => "Failed to send the message. Please try again later."]);
}
?>
