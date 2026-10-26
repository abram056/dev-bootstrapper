//! {{project_name}} binary entry point.

use {{snake_name}}_core::process;
use {{snake_name}}_proto::Message;

fn main() {
    let message = Message::new(1, "hello from {{project_name}}");
    println!("{}", process(&message));
}
