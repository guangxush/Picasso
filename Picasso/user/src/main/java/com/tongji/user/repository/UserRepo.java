package com.tongji.user.repository;

import com.tongji.user.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * @author: guangxush
 * @create: 2020/04/13
 */
@Repository
public interface UserRepo extends JpaRepository<User, Long> {

    Optional<User> findUserByUid(String uid);

}
