package com.tongji.mind.util;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static junit.framework.TestCase.assertNotNull;
import static org.junit.Assert.*;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class SSHWrapperTest {

    @Value("${config.target.port}")
    private int port;

    @Autowired
    private SSHWrapper sshWrapper;

    @Mock
    private JSch jsch;

    @Mock
    private Session session;

    @Before
    public void init() throws JSchException {
        Mockito.doNothing().when(jsch).addIdentity(Mockito.anyString());
        Mockito.when(jsch.getSession(Mockito.anyString(), Mockito.anyString()))
                .thenReturn(Mockito.mock(Session.class));
        Mockito.doNothing().when(session).connect();
        Mockito.when(session.openChannel(Mockito.anyString())).thenReturn(Mockito.mock(ChannelSftp.class));
    }

    @Test
    public void testPortValue(){
        Assert.assertEquals(port, 21122);
    }

    @Test
    public void testConnect() throws JSchException {
        assertNotNull(sshWrapper.connect());
    }
}