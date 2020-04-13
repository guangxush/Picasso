package com.tongji.common.util;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Calendar;
import java.util.Date;
import java.util.TimeZone;
import java.util.concurrent.TimeUnit;

public class DateUtil {

    /**
     * 根据日期字符串及Formatter获得Date
     *
     * @param str
     * @param formatter
     * @return
     */
    public static Date getDateFromStr(String str, DateTimeFormatter formatter) {
        LocalDateTime dateTime = LocalDateTime.parse(str, formatter);
        return Date.from(dateTime.atZone(ZoneId.systemDefault()).toInstant());
    }

    /**
     * 根据日期及Formatter获得字符串
     *
     * @param date
     * @param formatter
     * @return
     */
    public static String getStrFromDate(Date date, DateTimeFormatter formatter) {
        LocalDateTime dateTime = LocalDateTime.ofInstant(date.toInstant(), ZoneId.systemDefault());
        return dateTime.format(formatter);
    }

    /**
     * 获取日期
     *
     * @param second
     * @param minute
     * @param hour
     * @param day
     * @return
     */
    public static Date getDate(int second, int minute, int hour, int day) {
        Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone("GMT+8"));
        calendar.setTime(new Date());
        calendar.set(Calendar.HOUR_OF_DAY, hour);
        calendar.set(Calendar.MINUTE, minute);
        calendar.set(Calendar.SECOND, second);
        //day为-1表示前一天
        calendar.add(Calendar.DAY_OF_MONTH, day);
        Date date = calendar.getTime();
        return date;
    }

    /**
     * 检查时间差（绝对值）是否大于某数
     * <p>
     *
     * @param time1
     * @param time2
     * @return
     */
    public static boolean checkTimeDeltaGT(Date time1, Date time2, int delta, TimeUnit timeUnit) {
        long diffInMillies = Math.abs(time1.getTime() - time2.getTime());
        long expectedDeltaInMillies = TimeUnit.MILLISECONDS.convert(delta, timeUnit);
        if (diffInMillies > expectedDeltaInMillies) {
            return true;
        } else {
            return false;
        }
    }
}
