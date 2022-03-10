package com.application.waterbuddy;

/**
 * Message Class template for Firebase
 */
public class Message {

    public String source;
    public String dest;
    public String message;

    public Message(){
        // Default constructor required for dataSnapshot.getValue(Message.class)
    }

    public Message(String source, String dest, String message) {
        this.source = source;
        this.dest = dest;
        this.message = message;
    }
}
