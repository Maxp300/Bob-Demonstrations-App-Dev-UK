package com.electrify.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

/**
 * Security Configuration for Energy Grid System
 * 
 * DISCREPANCY #10: Using basic Spring Security instead of Auth0
 * Design document specifies:
 * - Auth0 as external identity server
 * - OAuth2 and OpenID Connect protocols
 * - Authorization Code Flow with PKCE
 * 
 * Current implementation uses basic Spring Security without Auth0 integration
 */
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        // DISCREPANCY #11: No API Gateway authentication pattern
        // Design specifies authentication should be at API Gateway level
        // Current implementation has security at service level
        
        http
            .csrf().disable()
            .authorizeRequests()
                .antMatchers("/api/public/**").permitAll()
                .antMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            .and()
            .httpBasic(); // DISCREPANCY #12: Using HTTP Basic instead of OAuth2/OIDC
        
        return http.build();
    }
    
    // DISCREPANCY #13: Missing Auth0 configuration
    // Should have Auth0 domain, client ID, client secret, audience configuration
    // Should implement PKCE flow for single page application
}

// Made with Bob
