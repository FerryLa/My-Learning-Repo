package com.ocean.testcrwaler.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
public class News {

    @Id
    @GeneratedValue
    private Long id;
    private String title;
    private String content;
    private String url;
    private String source;
    private LocalDateTime publishedAt;
}
