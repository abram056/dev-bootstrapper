//! Core logic for {{project_name}}.

use {{snake_name}}_proto::Message;

/// Processes a message and returns a formatted response.
pub fn process(message: &Message) -> String {
    format!("processed #{}: {}", message.id, message.payload)
}

#[cfg(test)]
mod tests {
    use super::*;
    use {{snake_name}}_proto::Message;

    #[test]
    fn process_message() {
        let m = Message::new(7, "ping");
        assert_eq!(process(&m), "processed #7: ping");
    }
}
