//! Shared types and protocol definitions for {{project_name}}.

/// A message exchanged between components.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Message {
    pub id: u64,
    pub payload: String,
}

impl Message {
    pub fn new(id: u64, payload: impl Into<String>) -> Self {
        Self {
            id,
            payload: payload.into(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn message_new() {
        let m = Message::new(1, "hello");
        assert_eq!(m.id, 1);
        assert_eq!(m.payload, "hello");
    }
}
