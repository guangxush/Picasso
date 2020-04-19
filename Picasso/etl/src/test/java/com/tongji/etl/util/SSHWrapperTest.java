package com.tongji.etl.util;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSch;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.Session;
import com.tongji.etl.model.ServerConfig;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import static junit.framework.TestCase.assertNotNull;

@RunWith(SpringJUnit4ClassRunner.class)
@SpringBootTest
public class SSHWrapperTest {
    @InjectMocks
    private SSHWrapper sshWrapper;

    @Mock
    private JSch jsch;

    @Mock
    private Session session;

    @Autowired
    private ServerConfig serverConfig;

    @Before
    public void init() throws JSchException {
        Mockito.doNothing().when(jsch).addIdentity(Mockito.anyString());
        Mockito.when(jsch.getSession(Mockito.anyString(), Mockito.anyString()))
                .thenReturn(Mockito.mock(Session.class));
        Mockito.doNothing().when(session).connect();
        Mockito.when(session.openChannel(Mockito.anyString())).thenReturn(Mockito.mock(ChannelSftp.class));
    }

    @Test
    public void testConnect() throws JSchException {
        assertNotNull(sshWrapper.connect(serverConfig));
    }
}