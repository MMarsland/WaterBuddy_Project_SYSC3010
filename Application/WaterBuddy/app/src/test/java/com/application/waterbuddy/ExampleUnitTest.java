package com.application.waterbuddy;

import org.junit.Test;

import static org.junit.Assert.*;

import android.content.Context;

/**
 * Example local unit test, which will execute on the development machine (host).
 *
 * @see <a href="http://d.android.com/tools/testing">Testing documentation</a>
 */
public class ExampleUnitTest {
    @Test
    public void addition_isCorrect() {
        assertEquals(4, 2 + 2);
    }


    @Test
    public void unit_test() {
        DatabaseInterface db = new DatabaseInterface();
        assertTrue(db.create_account("test", "123"));

        assertFalse(db.create_account("test", "123"));

        assertTrue(db.login("test", "123"));


    }
}