package com.application.waterbuddy;

import androidx.test.ext.junit.runners.AndroidJUnit4;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import static org.junit.Assert.*;

/**
 * Unit test for database behaviour
 *
 */
@RunWith(AndroidJUnit4.class)
public class UnitTest {
    private static DatabaseInterface db;

    @BeforeClass
    public static void setup() {
        db = new DatabaseInterface();
        db.delete_account("test");
        db.delete_account("test2");
    }

    /**
     * Create and attempt to log in to an account
     */
    @Test
    public void account_login() {
        db.sign_in();

        //delay for chance to read firebase
        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        assertTrue(db.create_account("test", "123"));

        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        assertFalse(db.create_account("test", "123"));

        try {
            Thread.sleep(3000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        assertFalse(db.login("test", "456"));
        assertTrue(db.login("test", "123"));
    }

    /**
     * Create a friend and attempt to add them to "test" friend list
     */
    @Test
    public void add_friend(){
        db.load("test");
        assertTrue(db.create_account("test2", "456"));

        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        assertEquals("Id does not exist", db.add_friend("Id_not_exist"));

        try {
            Thread.sleep(5000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        assertEquals("Friend successfully added", db.add_friend("test2"));
        assertTrue(db.register_station("test_station"));
    }
}
