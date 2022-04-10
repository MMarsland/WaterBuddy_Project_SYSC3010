package com.application.waterbuddy;

/**
 * Message Class template for Firebase
 */
public class Message {

    public String source;
    public String dest;
    public String message;

    /**
     * Default constructor required for dataSnapshot.getValue(Message.class)
     */
    public Message(){ }

    /**
     *
     * @param source String identifier naming the source of the message
     * @param dest String identifier naming the destination of the message
     * @param message The message itself
     */
    public Message(String source, String dest, String message) {
        this.source = source;
        this.dest = dest;
        this.message = message;
    }
}
