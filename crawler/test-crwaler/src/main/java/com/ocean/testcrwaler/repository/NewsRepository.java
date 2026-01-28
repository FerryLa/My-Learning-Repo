package com.ocean.testcrwaler.repository;

import com.ocean.testcrwaler.entity.News;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NewsRepository extends JpaRepository<News, Long> {
    boolean existsByUrl(String url);
}
