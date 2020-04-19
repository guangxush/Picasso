package com.tongji.etl.service;

import com.tongji.etl.util.MailSend;
import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterThrowing;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.beans.factory.annotation.Autowired;

/**
 * @author: guangxush
 * @create: 2020/04/17
 */
@Aspect
@Slf4j
public class LogAspect {

    @Autowired
    private MailSend mailSend;

    @Pointcut("execution(* com.tongji.etl.service.*.*(..))||execution(* com.tongji.etl.producer.*.*(..))")
    private void log() {

    }

    /**
     * AOP joinpoint to handle exception and send message using email
     * */
    @AfterThrowing(pointcut = "log()", throwing = "e")
    public void doAfterThrowing(JoinPoint joinPoint, Exception e) {
        String errMsg = "Errors " + e + " happened in Service: " + getMethodNameAndArgs(joinPoint);
        log.error(errMsg);
        //mailSend.sendmail(errMsg);
    }

    /**
     * Java reflect to get class info
     * */
    private String getMethodNameAndArgs (JoinPoint joinPoint) {
        Object[] args = joinPoint.getArgs();
        StringBuffer sb = new StringBuffer();
        sb.append(joinPoint.getTarget().getClass().getName() + "." + joinPoint.getSignature().getName());
        for (int i = 0; i < args.length;  i++ ) {
            sb.append(" arg[" + i + "]: " + args[i]);
        }
        return sb.toString();
    }
}
